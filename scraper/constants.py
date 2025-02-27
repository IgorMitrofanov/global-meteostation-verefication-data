# /constants.py

PARAMETERS_LIST = [
    {'mitype': '*IWS*', 
     'mititle': '*Датчики**комплексные**параметров**атмосферы*', 
     'path': 'data/all_years_IWS_Датчикикомплексныепараметроватмосферы.csv'},
    {'mitype': '*Vantage**Pro*', 
     'mititle': '*Станции*', 
     'path': 'data/all_years_VantagePro_Станции.csv'},
    {'mitype': '*WXT*', 
     'mititle': '*Метеостанции*', 
     'path': 'data/all_years_WXT_Метеостанции.csv'},
    {'mitype': '*PWS*', 
     'mititle': '*Метеостанции*', 
     'path' : 'data/all_years_PWS_Метеостанции.csv'},
    {'mitype': '*WS**UMB*', 
     'mititle': '*Станции*', 
     'path': 'data/all_years_WSUMB_Станции.csv'},
    {'mitype': '*М-49М*', 
     'mititle': '*Станции*', 
     'path': 'data/all_years_М-49М_Станции.csv'},
    {'mitype': '*СОКОЛ-М1*', 
     'mititle': '*Станции*', 
     'path': 'data/all_years_СОКОЛ-М1_Станции.csv'},
    {'mitype': '*ДВН*', 
     'mititle': '*Датчики**направления**ветра*', 
     'path' : 'data/all_years_ДВН_Датчикинаправленияветра.csv'},
    {'mitype': '*ДВС*', 
     'mititle': '*Датчики**скорости**ветра*', 
     'path' : 'data/all_years_ДВС_Датчикискоростиветра.csv'},
    {'mitype': '*ДО*', 
     'mititle': '*Датчики**осадков*', 
     'path': 'data/all_years_ДО_Датчикиосадков.csv'},
    {'mitype': '*ДТВ*', 
     'mititle': '*Датчики**температуры**и**влажности**воздуха*', 
     'path': 'data/all_years_ДТВ_Датчикитемпературыивлажностивоздуха.csv'},
    {'mitype': '*ДД*', 
     'mititle': '*Датчики**атмосферного**давления*', 
     'path': 'data/all_years_ДД_Датчикиатмосферногодавления.csv'},
    ]

DATA_URL = "https://fgis.gost.ru/fundmetrology/cm/xcdb/vri/select"

# Uploading time to schedule
HOURS_UPLOADING: int = 10
MINUTES_UPLOADING: int = 25
DAEMON_SLEEPING_TIME: int = 1

# Uploader 
UPLOADER_TIMEOUT: str = 0.5
ROWS_ON_PAGE: int = 100

# Data
ENCODING = "utf-8"
DATA_DIR = "data/"
