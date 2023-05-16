from res.artifacts import Res

RAW_DATA_FILE_NAME = "./offline_data/res_data.csv"
MODIFIED_FINAL_DATA_FILE_NAME = "./offline_data/res_offline_modified.csv"

# https://www.czso.cz/csu/res/registr_ekonomickych_subjektu
important_cols = [Res.ICO, Res.COBCE_TEXT, Res.ULICE_TEXT, Res.PSC, Res.FIRMA, Res.FORMA]
important_forms = [111, 112, 113, 117, 118, 121, 145, 161, 205, 301, 302, 313, 332, 352, 362, 381, 601, 641, 661, 706,
                   708, 721, 801, 804, 761, 771, 881, 961]
