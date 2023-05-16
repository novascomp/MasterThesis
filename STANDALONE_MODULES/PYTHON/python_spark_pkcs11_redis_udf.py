SLOT_ID=""
SO_PIN=""
SIMULATOR_PORT=""
TOKEN_NAME=""
TOKEN_PASSWORD=""
PKCS11_MODULE="/opt/workspace/libcs_pkcs11_R3.so"
CS_PKCS11_R3_CFG_1="/opt/workspace/cs_pkcs11_R3.cfg"
HSM_SIMULATOR_ADDRESS="utimaco_hsm_simulator"
HSM_SIMULATOR_PORT="3001"
NA_CHAR="-"

ENCODING="UTF-8"
STATIC_SALT=""
REDIS_HOST='spark_redis'
REDIS_PASSWORD=''
REDIS_PORT=6379

# SPARK
import os
SPARK_MASTER_HOST=os.environ.get('SPARK_MASTER_HOST')
SPARK_MASTER_PORT=os.environ.get('SPARK_MASTER_PORT')
SPARK_EXECUTOR_MEMORY=os.environ.get('SPARK_EXECUTOR_MEMORY')

import logging
import redis

from pkcs11 import KeyType, Attribute, ObjectClass, lib

from argparse import ArgumentParser

import logging

import binascii
import time

from pyspark.sql import SparkSession
import pyspark.sql.functions as f

from enum import Enum
from hashlib import sha256
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("-r", "--request", dest="request_id", help="request id")
parser.add_argument("-f", "--file", dest="filename", help="input file path")
parser.add_argument("-k", "--key", dest="key_label", help="key label")
parser.add_argument("-c", "--cols", dest="cols", help="cols to pseud")
parser.add_argument("-t", "--type", dest="type", help="pseud type")
parser.add_argument("-o", "--operation", dest="operation", help="pseud operation")
args = parser.parse_args()

class PseudType(Enum):
    ENCRYPT = "encrypt"
    HASH = "hash"

class PseudOperation(Enum):
    PSEUD = "pseud"
    DE_PSEUD = "de_pseud"

class EndpointTechnology(Enum):
    PANDAS_PKCS11 = "pandas_pkcs11"
    SPARK_PKCS11 = "spark_pkcs11"
    SPARK_REDIS = "spark_redis"

class PseudOptions:
    def __init__(self, pseud_type: PseudType, operation: PseudOperation, technology: EndpointTechnology,
                 key_label: str):
        self.operation: PseudOperation = operation
        self.pseud_type: PseudType = pseud_type
        self.technology: EndpointTechnology = technology
        self.key_label: str = key_label

class Commander:

    def __init__(self, request_id: str, file_path: str, col_names_to_pseud: list, pseud_options: PseudOptions):
        self.request_id = request_id
        self.col_names_to_pseud = col_names_to_pseud
        self.pseud_options = pseud_options
        self.file_path = file_path
        self.pseud_options = pseud_options

args.cols = args.cols.split()

if args.type.lower() == PseudType.ENCRYPT.value:
    args.type = PseudType.ENCRYPT
else:
    args.type = PseudType.HASH

if args.operation.lower() == PseudOperation.PSEUD.value:
    args.operation = PseudOperation.PSEUD
else:
    args.operation = PseudOperation.DE_PSEUD


options = PseudOptions(args.type, args.operation, EndpointTechnology.SPARK_REDIS, args.key_label)
commander = Commander(args.request_id, args.filename , args.cols, options)


def get_key(session, key_label: str, key_length=256):
    logging.info(f'PKCS #11 Retrieving key')
    key = get_key_by_label(session, key_label)
    if key is None:
        return generate_aes_key(session, key_length, True, key_label)
    else:
        return key


def get_key_by_label(session, label):
    logging.info(f'PKCS #11 Get key by label')
    for obj in session.get_objects({
        Attribute.CLASS: ObjectClass.SECRET_KEY,
        Attribute.LABEL: label,
    }):
        return obj


def generate_aes_key(session, key_length: int, store: bool, label: str):
    logging.info(f'Generating AES key')
    return session.generate_key(KeyType.AES, key_length, store=store, label=label, template={
        Attribute.SENSITIVE: False,
        Attribute.EXTRACTABLE: False
    })


def encrypt_aes(key, data, iv):
    return key.encrypt(data, mechanism_param=iv)


def decrypt_aes(key, data, iv):
    return key.decrypt(data, mechanism_param=iv)

def get_spark_instance(app_name: str):
    return SparkSession.builder.appName(app_name).getOrCreate()

def compute_hash(static_salt: str, dynamic_salt: str, plain_text: str):
    return sha256((static_salt + dynamic_salt + plain_text).encode(ENCODING)).hexdigest()

def get_hsm_session():
    os.environ['CS_PKCS11_R3_CFG'] = CS_PKCS11_R3_CFG_1
    os.environ['PKCS11_MODULE'] = PKCS11_MODULE
    return lib(PKCS11_MODULE).get_token(token_label=TOKEN_NAME).open(True, TOKEN_PASSWORD)

def get_redis():
    global redis_inst
    try:
        if redis_inst is not None:
            return redis_inst
    except:
        redis_inst = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT)
    return redis_inst

def pseud_redis(user_id, text, col_name):
    digest = compute_hash(STATIC_SALT, user_id + col_name, text)
    get_redis().set(digest, text)
    return digest

def de_pseud_redis(text):
    pre_de_pseud = get_redis().get(text)
    if pre_de_pseud is not None:
        return pre_de_pseud.decode(ENCODING)
    else:
        return "Data Missing in Redis!!!"

def pseud_hsm(user_id, text, key_label, col_name):
    global key
    try:
        if key is not None:
            pass
    except:
        key = get_key(get_hsm_session(), key_label)

    enc_bytes = encrypt_aes(key, text.encode(ENCODING), compute_hash(STATIC_SALT, user_id + col_name, '').encode(ENCODING)[:16])
    hex_val = binascii.hexlify(enc_bytes).decode(ENCODING)

    return hex_val

def de_pseud_hsm(user_id, text, key_label, col_name):
    global key
    try:
        if key is not None:
            pass
    except:
        key = get_key(get_hsm_session(), key_label)

    return decrypt_aes(key, binascii.unhexlify(text), compute_hash(STATIC_SALT, user_id + col_name, '').encode(ENCODING)[:16]).decode(ENCODING)

def append_col(commander: Commander, col_name: str, user_id_col_name: str, tmp_pseud_col: str, df, key_label=""):
    logging.info(f'{col_name}_{commander.pseud_options.operation.value}')
    operation = commander.pseud_options.operation
    pseud_type = commander.pseud_options.pseud_type

    if pseud_type == PseudType.HASH and operation == PseudOperation.PSEUD:
        pseud_redis_udf = f.udf(pseud_redis)
        df = df.withColumn(tmp_pseud_col, pseud_redis_udf(f.col(user_id_col_name), f.col(col_name), f.lit(col_name)))
    if pseud_type == PseudType.HASH and operation == PseudOperation.DE_PSEUD:
        retrieve_redis_udf = f.udf(de_pseud_redis)
        df = df.withColumn(tmp_pseud_col, retrieve_redis_udf(f.col(col_name)))
    if pseud_type == PseudType.ENCRYPT and operation == PseudOperation.PSEUD:
        pseud_pkcs11_udf = f.udf(pseud_hsm)
        df = df.withColumn(tmp_pseud_col, pseud_pkcs11_udf(f.col(user_id_col_name), f.col(col_name), f.lit(key_label), f.lit(col_name)))
    if pseud_type == PseudType.ENCRYPT and operation == PseudOperation.DE_PSEUD:
        de_pseud_pkcs11_udf = f.udf(de_pseud_hsm)
        df = df.withColumn(tmp_pseud_col, de_pseud_pkcs11_udf(f.col(user_id_col_name), f.col(col_name), f.lit(key_label), f.lit(col_name)))

    logging.info(f'{tmp_pseud_col} DONE')

    return df


def operate_given_cols(commander: Commander, id_col, df_default):
    pseud_type = commander.pseud_options.pseud_type
    key_label = commander.pseud_options.key_label
    print(key_label)

    tmp_id_col = 'tmp_id_col'
    df_final = df_default.select(id_col)
    df_original = df_default.withColumnRenamed(id_col, tmp_id_col)

    for col_name in commander.col_names_to_pseud:
        df_original = df_original.drop(col_name)
        tmp_pseud_col = f'{col_name}_{commander.pseud_options.operation.value}'
        df_tmp = df_default.select(f.col(id_col).alias(tmp_id_col), col_name)
        df_with_pseud_operation = append_col(commander, col_name, tmp_id_col, tmp_pseud_col, df_tmp, key_label)
        df_final = df_final.join(df_with_pseud_operation.select(tmp_id_col, f.col(tmp_pseud_col)
                                                                .alias(col_name)),
                                 df_final.id == df_with_pseud_operation.tmp_id_col).drop(tmp_id_col)


    return df_final.join(df_original, df_final.id == df_original.tmp_id_col).drop(tmp_id_col)


def spark_service(commander: Commander):
    id_col = "id"
    file_path = commander.file_path
    pseud_type = commander.pseud_options.pseud_type.value
    operation = commander.pseud_options.operation.value
    folder_name = f'{file_path}_SPARK_{pseud_type}_{operation}'

    logging.info(f'Starting SPARK service')
    logging.info(f'Request ID: {commander.request_id}')
    logging.info(f'Result folder name: {folder_name}')

    start = time.time()
    logging.info(f'Start time: {start}')
    spark = get_spark_instance(commander.request_id)
    df = spark.read.option("quote", "\"").option("escape", "\"").csv(commander.file_path, encoding=ENCODING, sep=",", header=True).na.fill(str(NA_CHAR))#.limit(10)
    df_cols_appended = operate_given_cols(commander, id_col, df)
    df_cols_appended.sort(f.col(id_col).cast('integer').asc()).coalesce(1) \
        .write.mode("overwrite").option("quote", "\"").option("escape", "\"").option("header", True).csv(folder_name)
    spark.stop()
    end = time.time()
    logging.info(f'End time: {end}')
    print(f'Final time: {end - start}')

    for p in Path(folder_name).glob('*.csv'):
        output_file_path = f'{folder_name}/{p.name}'
        logging.info(f'CSV result path: {output_file_path}')
        return

    logging.info(f'Failed')

spark_service(commander)