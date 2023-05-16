import requests
import json
import random

from airport_info import icao_all_codes_available, record_fields
from airport_info.artifacts import RAPID_API, AIRPORT_INFO


def connect_to_airport_info(icao: int, rapid_api_key) -> str:
    headers = {
        RAPID_API.KEY_FIELD: rapid_api_key,
        RAPID_API.HOST_FIELD: AIRPORT_INFO.DOMAIN
    }

    response = requests.request("GET", AIRPORT_INFO.URL, headers=headers, params={AIRPORT_INFO.PARAM_ICAO: icao})
    return json.loads(response.content)


def get_random_icao_codes(count: int):
    return random.sample(icao_all_codes_available, count)


def transform_record_raw_to_record(record_raw: dict) -> dict:
    record = dict()
    for field in record_fields:
        record[field] = record_raw[field]
    return record
