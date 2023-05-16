import logging
import os
import csv
from concurrent.futures import ThreadPoolExecutor

import requests
import subprocess

from artifacts import Commander
from rest_api_module import EncryptParserEnum, PseudOperation, PseudOptions, PseudType, EndpointTechnology, UploadType
from rest_api_module.settings import ENCODING, HDFS_PATH

executor = ThreadPoolExecutor(max_workers=1000)
encryption_source_locations_dict = dict()
pseud_locations_dict = dict()


def get_commander(args, request_id: str, pseud_options: PseudOptions, upload_path: str,
                  upload_type: UploadType) -> Commander:
    file_path = f'{upload_path}{request_id}.csv'
    cols_to_pseud = args[EncryptParserEnum.COL_NAMES_TO_PSEUD.value]
    file = args[EncryptParserEnum.FILE.value]

    if upload_type == upload_type.DIRECT or upload_type == upload_type.HDFS:
        encryption_source_locations_dict[request_id] = upload_type.value

    if upload_type == upload_type.HDFS:
        file_path = f'{upload_path}{args[EncryptParserEnum.FILE.value]}'

    if upload_type == upload_type.DIRECT:
        file.save(file_path)

    if upload_type == upload_type.HTTPS:
        source_location = args[EncryptParserEnum.FILE.value]
        encryption_source_locations_dict[request_id] = source_location
        download_csv(source_location, file_path)
    pseud_locations_dict[request_id] = None
    return Commander(request_id, file_path, cols_to_pseud, pseud_options)


def get_list_of_records(request_id, output_path):
    output_file_path = f'{output_path}{request_id}.csv'
    with open(output_file_path) as csv_file:
        records = csv.reader(csv_file, delimiter=',')
        return list(records)


# def remove_uploaded_file(request_id, upload_path):
#    if upload_path == HDFS_PATH:
#        runcmd(f'wget {location} -O {file_path}')
#    else:
#        input_file_path = f'{upload_path}{request_id}.csv'
#        os.remove(input_file_path)


def download_csv(location: str, file_path):
    runcmd(f'wget {location} -O {file_path}')
    logging.info(f'wget {location} -O {file_path}')
    # with requests.Session() as s:
    #    download = s.get(location, verify=False)
    #    decoded_content = download.content.decode(ENCODING)
    #    with open(file_path, 'w', encoding=ENCODING) as file:
    #        file.write(decoded_content)


def upload_file_to_storage(service_url, file_path) -> str:
    files = {'file': open(file_path, 'r', encoding=ENCODING)}
    getdata = requests.post(service_url, files=files)
    return getdata.headers.get("Location")


# https://colab.research.google.com/drive/1VyWXq_RAqeq-6UIiiM-3vpyKpIozKvsL?usp=sharing#scrollTo=CUblAJ757ZtE
def runcmd(cmd, verbose=True, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass


def get_pseud_options(technology: str, pseud_operation, key_label="none") -> PseudOptions:
    if technology == EndpointTechnology.PYTHON_SPARK_REDIS_UDF.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.HASH, PseudOperation.PSEUD, EndpointTechnology.PYTHON_SPARK_REDIS_UDF,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.HASH, PseudOperation.DE_PSEUD, EndpointTechnology.PYTHON_SPARK_REDIS_UDF,
                                key_label)

    if technology == EndpointTechnology.PYTHON_SPARK_PKCS11_UDF.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.PSEUD, EndpointTechnology.PYTHON_SPARK_PKCS11_UDF,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.DE_PSEUD, EndpointTechnology.PYTHON_SPARK_PKCS11_UDF,
                                key_label)

    if technology == EndpointTechnology.PYTHON_SPARK_REDIS_COLLECT.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.HASH, PseudOperation.PSEUD, EndpointTechnology.PYTHON_SPARK_REDIS_COLLECT,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.HASH, PseudOperation.DE_PSEUD, EndpointTechnology.PYTHON_SPARK_REDIS_COLLECT,
                                key_label)

    if technology == EndpointTechnology.PYTHON_SPARK_PKCS11_COLLECT.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.PSEUD, EndpointTechnology.PYTHON_SPARK_PKCS11_COLLECT,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.DE_PSEUD,
                                EndpointTechnology.PYTHON_SPARK_PKCS11_COLLECT,
                                key_label)

    if technology == EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.PSEUD, EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.DE_PSEUD,
                                EndpointTechnology.PYTHON_PANDAS_PKCS11_NONE, key_label)

    if technology == EndpointTechnology.SCALA_SPARK_CXI.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.PSEUD, EndpointTechnology.SCALA_SPARK_CXI,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.DE_PSEUD,
                                EndpointTechnology.SCALA_SPARK_CXI,
                                key_label)

    if technology == EndpointTechnology.SCALA_SPARK_JCE.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.PSEUD, EndpointTechnology.SCALA_SPARK_JCE,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.DE_PSEUD,
                                EndpointTechnology.SCALA_SPARK_JCE,
                                key_label)

    if technology == EndpointTechnology.SCALA_SPARK_PKCS11.value:
        if pseud_operation == PseudOperation.PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.PSEUD, EndpointTechnology.SCALA_SPARK_PKCS11,
                                key_label)

        if pseud_operation == PseudOperation.DE_PSEUD.value:
            return PseudOptions(PseudType.ENCRYPT, PseudOperation.DE_PSEUD,
                                EndpointTechnology.SCALA_SPARK_PKCS11,
                                key_label)

    raise Exception("Unsupported pseud_type/operation")
