from ares.artifacts import AresXMLElementParent, AresXMLElementChild, ARESRecord

ICOS_PATH = "./offline_data/icos.txt"
ico_list_pool = list()
soucasti_arr_parent = [AresXMLElementParent.SOUCASTI]
osobni_udaje_arr_parent = [AresXMLElementParent.OSOBNI_UDAJE]
zakladni_udaje_arr_parent = [AresXMLElementParent.ZAU]

osobni_udaje_arr_child = [AresXMLElementChild.TP, AresXMLElementChild.J, AresXMLElementChild.P]
zakladni_udaje_arr_child = [AresXMLElementChild.NAZEV]

record_fields = [ARESRecord.ICO, ARESRecord.COMPANY, ARESRecord.HEADQUARTERS, ARESRecord.DEGREE, ARESRecord.FIRST_NAME,
                 ARESRecord.LAST_NAME]
