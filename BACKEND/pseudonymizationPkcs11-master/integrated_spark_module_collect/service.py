import logging

import binascii
import time
import redis

from pyspark.sql import SparkSession
import pyspark.sql.functions as f

from hashlib import sha256
from pathlib import Path

from artifacts import Commander, GeneralModuleResponse
from pkcs11_modul.service import encrypt_aes, decrypt_aes, open_session, get_key
from rest_api_module import PseudOperation, PseudType, UploadType
from rest_api_module.settings import ENCODING, SPARK_MASTER_HOST, SPARK_MASTER_PORT, SPARK_EXECUTOR_MEMORY, STATIC_SALT, \
    NA_CHAR, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


def get_spark_instance(app_name: str):
    spark = SparkSession. \
        builder. \
        appName(app_name). \
        master(f'spark://{SPARK_MASTER_HOST}:{SPARK_MASTER_PORT}'). \
        config("spark.executor.memory", SPARK_EXECUTOR_MEMORY). \
        getOrCreate()
    return spark


def get_col_as_list(df, col_name: str):
    return df.select(f.collect_list(col_name)).first()[0]


def compute_hash(static_salt: str, dynamic_salt: str, plain_text: str):
    return sha256((static_salt + dynamic_salt + plain_text).encode(ENCODING)).hexdigest()


def append_col(spark: SparkSession, redis_inst, commander: Commander, col_name: str, user_id_col_name: str, df,
               key=None):
    data = []
    tmp_id_col_name = f'{user_id_col_name}_tmp'
    schema = [tmp_id_col_name, f'{col_name}_{commander.pseud_options.operation.value}']
    logging.info(f'{col_name}_{commander.pseud_options.operation.value}')

    # PKCS#11
    for text, user_id in zip(get_col_as_list(df, col_name), get_col_as_list(df, user_id_col_name)):
        operation = commander.pseud_options.operation

        # Redis
        if key is None and operation == PseudOperation.PSEUD:
            str_computed_hash = compute_hash(STATIC_SALT, user_id + col_name, text)
            redis_inst.set(str_computed_hash, text)
            data.append([user_id, str_computed_hash])
        if key is None and operation == PseudOperation.DE_PSEUD:
            pre_de_pseud = redis_inst.get(text)
            if pre_de_pseud is not None:
                de_pseud = redis_inst.get(text).decode(ENCODING)
                data.append([user_id, de_pseud])
            else:
                data.append([user_id, "Data Missing in Redis!!!"])

        # PKCS#11
        if key is not None and operation == PseudOperation.PSEUD:
            enc_bytes = encrypt_aes(key, text.encode(ENCODING), compute_hash(STATIC_SALT, user_id + col_name, '').encode(ENCODING)[:16])
            hex_val = binascii.hexlify(enc_bytes).decode(ENCODING)
            data.append([user_id, hex_val])

        if key is not None and operation == PseudOperation.DE_PSEUD:
            dec_text = decrypt_aes(key, binascii.unhexlify(text), compute_hash(STATIC_SALT, user_id + col_name, '').encode(ENCODING)[:16]) \
                .decode(ENCODING)
            data.append([user_id, dec_text])

    df_with_pseud_operation = spark.createDataFrame(data, schema)
    return df.join(df_with_pseud_operation, df.id == df_with_pseud_operation.id_tmp).drop(tmp_id_col_name)


def operate_given_cols(spark, redis_inst, commander: Commander, id_col, df):
    pseud_type = commander.pseud_options.pseud_type

    key = None
    if pseud_type == PseudType.ENCRYPT:
        session = open_session()
        key = get_key(session, commander.pseud_options.key_label)

    for col_name in commander.col_names_to_pseud:
        df = append_col(spark, redis_inst, commander, col_name, id_col, df, key)

    if key is not None:
        session.close()

    return df


def spark_service_collect(commander: Commander, upload_type: UploadType) -> GeneralModuleResponse:
    logging.info(f'Starting SPARK service')
    id_col = "id"
    file_path = commander.file_path
    pseud_type = commander.pseud_options.pseud_type.value
    operation = commander.pseud_options.operation.value
    folder_name = f'{file_path}_SPARK_{pseud_type}_{operation}'

    logging.info(f'Request ID: {commander.request_id}')
    logging.info(f'Result folder name: {folder_name}')
    logging.info(f'Key label: {commander.pseud_options.key_label}')

    start = time.time()
    logging.info(f'Start time: {start}')
    spark = get_spark_instance(commander.request_id)
    df = spark.read.option("quote", "\"").option("escape", "\"").csv(commander.file_path, encoding=ENCODING, sep=",",
                                                                     header=True).na.fill(str(NA_CHAR))
    redis_inst = redis.Redis(host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT)
    df_cols_appended = operate_given_cols(spark, redis_inst, commander, id_col, df)
    df_original_dropped = df_cols_appended.drop(*commander.col_names_to_pseud)
    for col in commander.col_names_to_pseud:
        df_original_dropped = df_original_dropped.withColumnRenamed(f'{col}_{operation}', col)
    df_original_dropped.sort(f.col(id_col).cast('integer').asc()).coalesce(1) \
        .write.mode("overwrite").option("quote", "\"").option("escape", "\"").option("header", True).csv(folder_name,
                                                                                                         encoding=ENCODING)
    spark.stop()
    end = time.time()
    logging.info(f'End time: {end}')

    if upload_type is not upload_type.HDFS:
        for p in Path(folder_name).glob('*.csv'):
            output_file_path = f'{folder_name}/{p.name}'
            logging.info(f'CSV result path: {output_file_path}')
            return GeneralModuleResponse(start, end, output_file_path)

    return GeneralModuleResponse(start, end, folder_name)
