import pandas as pd
from integrated_pandas_module.artifacts import IvCrypto, EncryptedCrypto
from rest_api_module.settings import NA_CHAR


def encrypt_list_of_records(key, col_records: list, ivs_list: list) -> list:
    return [EncryptedCrypto(key, record, ivs_list[index]) for index, record in enumerate(col_records)]


def encrypt_df(key, df, col_names: list, ivs_list: list) -> list:
    col_to_encrypt = [df[col_name].fillna(str(NA_CHAR)).tolist() for col_name in col_names]
    return [encrypt_list_of_records(key, col, ivs_list) for col in col_to_encrypt]


def check_col_names(df_to_encrypt, col_names_to_encrypt: list):
    col_names_to_encrypt_set = set(col_names_to_encrypt)
    assert (col_names_to_encrypt_set == set(df_to_encrypt.columns).intersection(col_names_to_encrypt_set))


def encrypt(session, key, df_to_encrypt, col_names_to_encrypt: list, iv_col_name: str):
    check_col_names(df_to_encrypt, col_names_to_encrypt)
    df_encrypted = df_to_encrypt
    crypto_ivs = [IvCrypto(session) for _ in range(len(df_to_encrypt))]
    encrypted_cols = get_encrypted_cols(key, df_to_encrypt, col_names_to_encrypt, crypto_ivs)

    for index, col in enumerate(encrypted_cols):
        df_encrypted.drop(col_names_to_encrypt[index], inplace=True, axis=1)
        new_encrypted_column = pd.DataFrame([encrypted_crypto.as_hex_val() for encrypted_crypto in col])
        new_encrypted_column.columns = [col_names_to_encrypt[index]]
        df_encrypted = pd.concat([df_encrypted, new_encrypted_column], axis=1)

    return pd.concat([df_encrypted, get_ivs_df(ivs_to_hex_values(crypto_ivs), iv_col_name)], axis=1)


def get_encrypted_cols(key, df_to_encrypt, col_names_to_encrypt, crypto_ivs):
    return [encrypted_crypto_list for encrypted_crypto_list in
            encrypt_df(key, df_to_encrypt, col_names_to_encrypt, crypto_ivs)]


def ivs_to_hex_values(crypto_ivs: list) -> list:
    return [iv.as_hex_val() for iv in crypto_ivs]


def get_ivs_df(ivs_list: list, iv_col_name: str):
    df_iv = pd.DataFrame(ivs_list)
    df_iv.columns = [iv_col_name]
    return df_iv
