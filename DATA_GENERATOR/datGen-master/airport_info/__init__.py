# https://wikijii.com/wiki/List_of_airports_by_ICAO_code:_L#LK_%E2%80%93_Czech_Republic
from airport_info.artifacts import AirportRecord

icao_cz_codes_available = ["LKHO", "LKKU", "LKKV", "LKMR", "LKMT", "LKOL", "LKPD", "LKPO", "LKPR", "LKTB", "LKVO",
                           "LKZA"]

# https://cs.wikipedia.org/wiki/Leti%C5%A1t%C4%9B
icao_largest_according_to_persons_transported = ["KATL", "ZBAA", "OMDB", "KLAX", "RJTT", "KORD", "EGLL", "VHHH", "ZSPD",
                                                 "LFPG"]

icao_largest_according_to_volume_of_cargo_transported = ["KMEM", "RKSI", "PANC", "OMDB", "KSDF", "RCTP", "RJAA", "KLAX"]

icao_all_codes_available = icao_cz_codes_available + icao_largest_according_to_persons_transported \
                           + icao_largest_according_to_volume_of_cargo_transported

record_fields = [AirportRecord.PHONE, AirportRecord.LOCATION, AirportRecord.STREET, AirportRecord.CITY,
                 AirportRecord.COUNTRY, AirportRecord.POSTAL_CODE]
