from ares.transformations import connect_to_ares, get_record, get_random_ico_s, load_icos_pool


def get_online_json_ares_pool_records(count: int) -> list():
    load_icos_pool()
    records = list()
    for ico in get_random_ico_s(count):
        content = connect_to_ares(ico)
        record = get_record(content, ico)
        records.append(record)
    return records

# write_csv("test.csv", records)
