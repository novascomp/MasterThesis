import logging

import pandas as pd
import time

from pkcs11_modul.service import open_session, get_key
from integrated_pandas_module.encrypt import encrypt as core_encrypt
from integrated_pandas_module.decrypt import decrypt as core_decrypt
from artifacts import Commander, GeneralModuleResponse
from rest_api_module import PseudOperation
from rest_api_module.settings import ENCODING

iv_col_name = "iv"


def pandas_pkcs11_service(commander: Commander, output_path: str) -> GeneralModuleResponse:
    logging.info(f'Starting pseud_pandas_pkcs11')
    start = time.time()
    logging.info(f'Start time: {start}')
    session = open_session()
    pseud_operation = commander.pseud_options.operation
    key = get_key(session, commander.pseud_options.key_label)
    df = pd.read_csv(commander.file_path, encoding=ENCODING)
    cols_to_operate = commander.col_names_to_pseud

    if pseud_operation == PseudOperation.PSEUD:
        df_pseud = core_encrypt(session, key, df, cols_to_operate, iv_col_name)

    if pseud_operation == PseudOperation.DE_PSEUD:
        df_pseud = core_decrypt(session, key, df, cols_to_operate, iv_col_name)

    session.close()
    output_file_path = write_result(df_pseud, commander.request_id, output_path)
    end = time.time()
    logging.info(f'End time: {end}')
    return GeneralModuleResponse(start, end, output_file_path)


def write_result(df_encrypted, request_id, output_path):
    output_file_path = f'{output_path}{request_id}.csv'
    df_encrypted.to_csv(output_file_path, index=False)
    return output_file_path
