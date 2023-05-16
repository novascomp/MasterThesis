import logging

import time

from pathlib import Path

from artifacts import Commander, GeneralModuleResponse
from rest_api_module import UploadType
from rest_api_module.service import runcmd
from rest_api_module.settings import SPARK_MASTER_HOST, SPARK_MASTER_PORT, SPARK_EXECUTOR_MEMORY


def spark_service(commander: Commander, upload_type: UploadType) -> GeneralModuleResponse:
    logging.info(f'Starting SPARK service')
    file_path = commander.file_path
    request_id = commander.request_id
    pseud_type = commander.pseud_options.pseud_type.value
    operation = commander.pseud_options.operation.value
    key_label = commander.pseud_options.key_label
    technology = commander.pseud_options.technology
    output_path = f'{file_path}_SPARK_{pseud_type}_{operation}'

    logging.info(f'Request ID: {request_id}')
    logging.info(f'Result folder name: {output_path}')
    logging.info(f'Key label: {key_label}')

    start = time.time()
    logging.info(f'Start time: {start}')
    if technology == technology.SCALA_SPARK_CXI or technology == technology.SCALA_SPARK_JCE or technology == technology.SCALA_SPARK_PKCS11:
        api = technology.value.split("_")[2]
        env = "testEnv"
        cols_to_pseud = ",".join([str(elem) for elem in commander.col_names_to_pseud])
        cmd_command = f'spark-submit --master spark://{SPARK_MASTER_HOST}:{SPARK_MASTER_PORT} --conf \'spark.executor.extraJavaOptions=-Dapi={api} -Denv={env}\' --conf \'spark.driver.extraJavaOptions=-Dapi={api} -Denv={env}\' --executor-memory {SPARK_EXECUTOR_MEMORY} --num-executors 2 /opt/workspace/scala_cxi.jar {request_id} {file_path} {key_label} {cols_to_pseud} {operation} {output_path} id csv 10000 1'
        logging.info(cmd_command)
        runcmd(cmd_command)
    else:
        cols_to_pseud = " ".join([str(elem) for elem in commander.col_names_to_pseud])
        cmd_command = f'spark-submit --class org.apache.spark.example.SparkPi --master spark://{SPARK_MASTER_HOST}:{SPARK_MASTER_PORT} --executor-memory {SPARK_EXECUTOR_MEMORY} --num-executors 2 /opt/workspace/standalone_python_module.py -r {request_id} -f {file_path} -k {key_label} -c "{cols_to_pseud}" -t {pseud_type} -o {operation}'
        logging.info(cmd_command)
        runcmd(cmd_command)

    end = time.time()
    logging.info(f'End time: {end}')

    if upload_type is not upload_type.HDFS:
        for p in Path(output_path).glob('*.csv'):
            output_file_path = f'{output_path}/{p.name}'
            logging.info(f'Files written')
            logging.info(f'CSV result path: {output_file_path}')
            return GeneralModuleResponse(start, end, output_file_path)
        return None
    else:
        return GeneralModuleResponse(start, end, output_path)
