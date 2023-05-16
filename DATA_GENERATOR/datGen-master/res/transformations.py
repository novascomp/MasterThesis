import pandas as pd

from res import important_cols, important_forms, RAW_DATA_FILE_NAME, MODIFIED_FINAL_DATA_FILE_NAME
from settings import ENCODING


def get_modified_final_data():
    return pd.read_csv(MODIFIED_FINAL_DATA_FILE_NAME, encoding=ENCODING)


def clean_raw_data():
    df = pd.read_csv(RAW_DATA_FILE_NAME, encoding=ENCODING)
    df_modified = df[important_cols]
    df_modified_final = df_modified[df_modified.FORMA.isin(important_forms)].dropna()
    df_modified_final.to_csv(MODIFIED_FINAL_DATA_FILE_NAME)
