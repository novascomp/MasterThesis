import pandas as pd
from integrated_pandas_module.artifacts import IvCrypto, DecryptedCrypto


def decrypt_list_of_hex_vals(session, key, col_records: list, col_iv: list) -> list:
    return [DecryptedCrypto(key, record, IvCrypto(session, col_iv[index])) for index, record in enumerate(col_records)]


def decrypt_df(session, key, df, col_names: list, col_iv: list) -> list:
    cols_list = [df[col_name].tolist() for col_name in col_names]
    return [decrypt_list_of_hex_vals(session, key, col, col_iv) for col in cols_list]


def decrypt(session, key, df_to_decrypt, col_names_to_decrypt: list, iv_col_name: str):
    df_decrypted = df_to_decrypt
    df_iv = df_to_decrypt[iv_col_name]
    cols_to_decrypt = get_decrypted_cols(session, key, df_to_decrypt, col_names_to_decrypt, df_iv)

    for index, col in enumerate(cols_to_decrypt):
        df_decrypted.drop(col_names_to_decrypt[index], inplace=True, axis=1)
        new_decrypted_column = pd.DataFrame([decrypted_crypto.value.decode() for decrypted_crypto in col])
        new_decrypted_column.columns = [col_names_to_decrypt[index]]
        df_decrypted = pd.concat([df_decrypted, new_decrypted_column], axis=1)
    return df_decrypted


def get_decrypted_cols(session, key, df_to_decrypt, col_names_to_decrypt, df_iv):
    return [decrypted_list for decrypted_list in
            decrypt_df(session, key, df_to_decrypt, col_names_to_decrypt, df_iv)]
