import uuid

from ares.ares_main import get_online_json_ares_pool_records
from airport_info.airport_main import get_online_json_airport_info_pool_records
from res.res_main import get_offline_df_res_data_pool_records

from generator import get_generated_data_file_name
from generator.DataPool import DataPool
from generator.transformations import write_csv, gen_record


def init_pool(ares_pool_size, airport_pool_size, rapid_api_key) -> DataPool:
    ares_records = get_online_json_ares_pool_records(ares_pool_size)
    airport_records = get_online_json_airport_info_pool_records(airport_pool_size, rapid_api_key)
    df_res_data = get_offline_df_res_data_pool_records()
    return DataPool(ares_records, airport_records, df_res_data)


def generate_samples(sample_size: int, data_pool: DataPool) -> str:
    gen_records = list()
    for sample_id in range(sample_size):
        record = gen_record(sample_id, data_pool)
        gen_records.append(record)
    file_id = uuid.uuid4().hex
    write_csv(get_generated_data_file_name(file_id), gen_records)
    return file_id
