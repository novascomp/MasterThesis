import random
import requests

import xml.etree.ElementTree as ET

from ares import osobni_udaje_arr_child, zakladni_udaje_arr_child, osobni_udaje_arr_parent, zakladni_udaje_arr_parent, \
    soucasti_arr_parent, ico_list_pool, ICOS_PATH
from ares.artifacts import ARES, AresXMLElementChild, ARESRecord
from settings import ENCODING


def load_icos_pool():
    with open(ICOS_PATH, 'r', encoding=ENCODING) as f:
        for line in f.readlines():
            ico_list_pool.append(line)


def connect_to_ares(ico: int) -> str:
    r = requests.get(url=ARES.URL, params={ARES.PARAM_ICO: ico})
    content = r.content
    r.close()
    return content


def get_record(content, ico: int):
    record_raw = init_record_raw(ico)
    e = ET.fromstring(content)
    for elt in e.iter():
        att = elt.tag.split("}")[1].upper()

        if att in osobni_udaje_arr_parent:
            get_element(elt, osobni_udaje_arr_child, record_raw)

        if att in zakladni_udaje_arr_parent:
            get_element(elt, zakladni_udaje_arr_child, record_raw)

        if att in soucasti_arr_parent:
            break

    return transform_record_raw_to_record(record_raw)


def transform_record_raw_to_record(record_raw: dict) -> dict:
    record = dict()
    record[ARESRecord.ICO] = record_raw[ARESRecord.ICO].strip().replace("\n", "")
    record[ARESRecord.COMPANY] = check_and_get(record_raw[AresXMLElementChild.NAZEV], 0)
    record[ARESRecord.HEADQUARTERS] = check_and_get(record_raw[AresXMLElementChild.NAZEV], 1)
    record[ARESRecord.DEGREE] = check_and_get(record_raw[AresXMLElementChild.TP], 0)
    record[ARESRecord.FIRST_NAME] = check_and_get(record_raw[AresXMLElementChild.J], 0)
    record[ARESRecord.LAST_NAME] = check_and_get(record_raw[AresXMLElementChild.P], 0)
    return record


def check_and_get(element, index) -> str:
    try:
        return element[index].strip().replace("\n", "")
    except IndexError:
        return None


def get_element(element, required_elements, record_raw: dict):
    for elt in element.iter():
        att = elt.tag.split("}")[1].upper()
        if att in required_elements:
            record_raw[att].append(elt.text)


def get_random_ico_s(count: int):
    return random.sample(ico_list_pool, count)


def init_record_raw(ico: int) -> dict:
    record_raw = dict()
    record_raw[ARESRecord.ICO] = ico
    for attribute in (zakladni_udaje_arr_child + osobni_udaje_arr_child):
        record_raw[attribute] = list()
    return record_raw
