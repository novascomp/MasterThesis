from airport_info.transformation import get_random_icao_codes, connect_to_airport_info, transform_record_raw_to_record


def get_online_json_airport_info_pool_records(count: int, rapid_api_key) -> list():
    records = list()
    for index, icao in enumerate(get_random_icao_codes(count)):
        record_raw = connect_to_airport_info(icao, rapid_api_key)
        record = transform_record_raw_to_record(record_raw)
        records.append(record)
    return records
