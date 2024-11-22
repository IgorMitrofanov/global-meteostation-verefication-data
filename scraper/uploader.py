# /uploading.py

import os
import requests
import pandas as pd
import time
from typing import Dict, Any
import json
from scraper.constants import DATA_URL, UPLOADER_TIMEOUT, ROWS_ON_PAGE
from scraper.logger import get_logger

logger = get_logger(__name__)

def get_df(url: str, filter_params: Dict[str, Any]) -> pd.DataFrame:
    response = requests.get(url, params=filter_params)
    if response.status_code == 200:
        try:
            data = response.json()
            docs = data.get('response', {}).get('docs', [])
            df = pd.DataFrame(docs)
            return df
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
    else:
        logger.error(f"Request failed with status code {response.status_code}")
    return pd.DataFrame()  # Вернуть пустой DataFrame в случае ошибки


def get_df_by_the_filter(mitype, mititle, year='*'):
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
            'rows': ROWS_ON_PAGE,
            'start': page * ROWS_ON_PAGE
        }

        df = get_df(url=DATA_URL, filter_params=filter_params)

        if df.empty:
            break

        logger.debug(f'Page: {page}')
        logger.debug('Preview:')
        logger.debug(df)
        rows_appended += df.shape[0]
        logger.debug(f'Lines saved: {rows_appended}.')

        all_data = pd.concat([all_data, df], ignore_index=True)

        page += 1
        time.sleep(UPLOADER_TIMEOUT)

    if year == '*':
        year = 'all_years'
        
    mitype = mitype.replace('*', '')
    mititle = mititle.replace('*', '')
    logger.info(f"uploaded rows: {rows_appended}")
    return all_data