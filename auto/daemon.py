import requests
import pandas as pd
import time

from typing import Dict, Any

from auto.constants import PARAMETERS_LIST, DATA_URL
from auto.logger import get_logger

logger = get_logger(__name__)


def get_df(url: str, filter_params: Dict[Any]) -> pd.DataFrame:
    response = requests.get(url, params=filter_params)
    data = response.json()
    docs = data['response']['docs']
    df = pd.DataFrame(docs)
    return df


def uploading_by_the_filter(mitype, mititle, year='*'):
    page = 0
    filter_value = f'verification_year:{year} AND mi.mitype:{mitype} AND mi.mititle:{mititle}'


    rows_appended = 0
    all_data = pd.DataFrame()

    while True:
        filter_params = {
            'fq': f'{filter_value}',
            'q': '*',
            'fl': '*',
            'sort': 'verification_date desc,org_title asc',
            'rows': 100,
            'start': page * 100
        }

        df = get_df(url=DATA_URL, filter_params=filter_params)

        if df.empty:
            break

        logger.debug(f'Page: {page}')
        logger.debug('Preview:')
        logger.debug(df)
        rows_appended += df.shape[0]
        logger.info(f'Lines saved: {rows_appended}.')

        all_data = pd.concat([all_data, df], ignore_index=True)

        page += 1
        time.sleep(0.25)

    if year == '*':
        year = 'all_years'
    mitype = mitype.replace('*', '')
    mititle = mititle.replace('*', '')

    all_data.to_csv(f'data/{year}_{mitype}_{mititle}.csv', index=False, encoding='utf-8')

if __name__ == '__main__':
    for params in PARAMETERS_LIST:
        logger.info('Uploading by the filter: ', params['mitype'], params['mititle'])
        uploading_by_the_filter(params['mitype'], params['mititle'])
        time.sleep(0.25)
        df= pd.read_csv(params['path'], encoding='utf-8')
        df = pd.concat([df])

    df.to_csv('data/all_data.csv', index=False, encoding='utf-8')
    logger.info('Данные сохранены в csv.')