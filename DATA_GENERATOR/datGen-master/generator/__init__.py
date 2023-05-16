import airport_info
import ares
from generator.artifacts import Sample

MAX_SAMPLE_SIZE = 100000
MIN_SAMPLE_SIZE = 1
GENERATED_DATA_ROOT = "./"
GENERATED_DATA_FOLDER = "generated"
csv_fields = [Sample.ID] + ares.record_fields + airport_info.record_fields


def get_generated_data_file_name(id):
    return f'{GENERATED_DATA_ROOT}{GENERATED_DATA_FOLDER}/{id}.csv'
