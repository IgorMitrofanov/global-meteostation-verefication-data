import requests
import pandas as pd
import time

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

        print(f'Страница: {page}')
        print('Предпросмотр:')
        print(df)
        rows_appended += df.shape[0]
        print(f'Строк сохранено: {rows_appended}')

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
        print('Выгрузка: ', params['mitype'], params['mititle'])
        main(params['mitype'], params['mititle'])
        time.sleep(0.25)

