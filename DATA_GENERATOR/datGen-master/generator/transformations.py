import csv
import random

import names

from airport_info import AirportRecord
from ares import ARESRecord
from generator import csv_fields
from generator.DataPool import DataPool
from generator.artifacts import Sample
from res import Res
from settings import ENCODING


def gen_record(id: int, data_pool: DataPool) -> dict:
    ares_rec_len: int = len(data_pool.ares_records)
    airport_rec_len: int = len(data_pool.airport_records)
    ares_rand_index = random.randint(0, ares_rec_len - 1)
    airport_rand_index = random.randint(0, airport_rec_len - 1)
    record = create_record(id, data_pool.ares_records[ares_rand_index], data_pool.airport_records[airport_rand_index])
    replace_real_names_by_random(record)
    replace_company(record, data_pool.df_res_data)
    return record


def replace_real_names_by_random(record):
    record[ARESRecord.FIRST_NAME] = names.get_first_name()
    record[ARESRecord.LAST_NAME] = names.get_last_name()


def replace_company(record, df_res_data):
    data_len = df_res_data.shape[0]
    if replacement_heuristic():
        index = random.randint(0, data_len - 1)
        record[ARESRecord.ICO] = df_res_data.iloc[index][Res.ICO]
        record[ARESRecord.COMPANY] = df_res_data.iloc[index][Res.FIRMA]
        record[AirportRecord.LOCATION] = df_res_data.iloc[index][Res.COBCE_TEXT]
        record[AirportRecord.STREET] = df_res_data.iloc[index][Res.ULICE_TEXT]
        record[AirportRecord.POSTAL_CODE] = df_res_data.iloc[index][Res.PSC]


def create_record(id, ares_record, airport_record):
    return {Sample.ID: id} | ares_record | airport_record


def write_csv(file_name, records):
    with open(file_name, 'w', newline='', encoding=ENCODING) as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(records)


def replacement_heuristic():
    return random.randint(1, 2) % 2 == 0
