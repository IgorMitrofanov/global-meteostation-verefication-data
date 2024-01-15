import requests
import pandas as pd
import time

from auto.logger import get_logger

logger = get_logger(__name__)

# Функция для отправки запроса и получения данных
def get_data(params):
    url = "https://fgis.gost.ru/fundmetrology/cm/xcdb/vri/select"
    response = requests.get(url, params=params)
    data = response.json()
    docs = data['response']['docs']
    df = pd.DataFrame(docs)
    return df

def main(mitype, mititle, year='*'):
    page = 0
    filter_value = f'verification_year:{year} AND mi.mitype:{mitype} AND mi.mititle:{mititle}'


    rows_appended = 0
    all_data = pd.DataFrame()

    while True:
        params = {
            'fq': f'{filter_value}',
            'q': '*',
            'fl': '*',
            'sort': 'verification_date desc,org_title asc',
            'rows': 100,
            'start': page * 100
        }

        df = get_data(params)

        if df.empty:
            break

        logger.debug(f'Страница: {page}')
        logger.debug('Предпросмотр:')
        logger.debug(df)
        rows_appended += df.shape[0]
        logger.info(f'Строк сохранено: {rows_appended}')

        all_data = pd.concat([all_data, df], ignore_index=True)

        page += 1
        time.sleep(0.25)

    if year == '*':
        year = 'all_years'
    mitype = mitype.replace('*', '')
    mititle = mititle.replace('*', '')

    all_data.to_csv(f'data/{year}_{mitype}_{mititle}.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    parameters_list = [
    {'mitype': '*IWS*', 'mititle': '*Датчики**комплексные**параметров**атмосферы*'},
    {'mitype': '*Vantage**Pro*', 'mititle': '*Станции*'},
    {'mitype': '*WXT*', 'mititle': '*Метеостанции*'},
    {'mitype': '*PWS*', 'mititle': '*Метеостанции*'},
    {'mitype': '*WS**UMB*', 'mititle': '*Станции*'},
    {'mitype': '*М-49М*', 'mititle': '*Станции*'},
    {'mitype': '*СОКОЛ-М1*', 'mititle': '*Станции*'},
    {'mitype': '*ДВН*', 'mititle': '*Датчики**направления**ветра*'},
    {'mitype': '*ДВС*', 'mititle': '*Датчики**скорости**ветра*'},
    {'mitype': '*ДО*', 'mititle': '*Датчики**осадков*'},
    {'mitype': '*ДТВ*', 'mititle': '*Датчики**температуры**и**влажности**воздуха*'},
    {'mitype': '*ДД*', 'mititle': '*Датчики**атмосферного**давления*'},
    ]
    for params in parameters_list:
        logger.info('Выгрузка: ', params['mitype'], params['mititle'])
        main(params['mitype'], params['mititle'])
        time.sleep(0.25)
        df_davis = pd.read_csv('data/all_years_VantagePro_Станции.csv', encoding='utf-8')
        df_vaisala = pd.read_csv('data/all_years_WXT_Метеостанции.csv', encoding='utf-8')
        df_icb = pd.read_csv('data/all_years_PWS_Метеостанции.csv', encoding='utf-8')
        df_lufft = pd.read_csv('data/all_years_WSUMB_Станции.csv', encoding='utf-8')
        df_safonovskiy = pd.read_csv('data/all_years_М-49М_Станции.csv', encoding='utf-8')
        df_sokol = pd.read_csv('data/all_years_СОКОЛ-М1_Станции.csv', encoding='utf-8')

        # Минимакс-94
        df_dvn = pd.read_csv('data/all_years_ДВН_Датчикинаправленияветра.csv', encoding='utf-8')
        df_dvs = pd.read_csv('data/all_years_ДВС_Датчикискоростиветра.csv', encoding='utf-8')
        df_dd = pd.read_csv('data/all_years_ДД_Датчикиатмосферногодавления.csv', encoding='utf-8')
        df_do = pd.read_csv('data/all_years_ДО_Датчикиосадков.csv', encoding='utf-8')
        df_dtv = pd.read_csv('data/all_years_ДТВ_Датчикитемпературыивлажностивоздуха.csv', encoding='utf-8')

        df_minimax = pd.concat([df_dvn, df_dvs, df_dd, df_do, df_dtv])

        df_burstroy = pd.read_csv('data/all_years_IWS_Датчикикомплексныепараметроватмосферы.csv', encoding='utf-8')

        df_all = pd.concat([df_davis, df_vaisala, df_icb, df_lufft, df_safonovskiy, df_sokol, df_minimax, df_burstroy])

        df_all.to_csv('data/all_data.csv', index=False, encoding='utf-8')
        logger.info('Данные сохранены в csv.')