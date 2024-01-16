# /daemon.py

from scheduler import Scheduler

from db.mongodb_manager import MongoDBManager
from uploader import uploading_by_the_filter
from constants import PARAMETERS_LIST, HOURS_UPLOADING, MINUTES_UPLOADING, DAEMON_SLEEPING_TIME, \
    DB_NAME, DB_HOST, DB_PORT, DB_MAIN_TABLE_NAME
import time
import datetime
import pandas as pd

from logger import get_logger

logger = get_logger(__name__)


def run_uploader():
    try:
        all_data = pd.DataFrame()
        for params in PARAMETERS_LIST:
            logger.info(f'Uploading by the filter: {params['mitype'], params['mititle']}')
            uploading_by_the_filter(params['mitype'], params['mititle'])
            time.sleep(0.25)
            df = pd.read_csv(params['path'], encoding='utf-8')
            all_data = pd.concat([all_data, df], ignore_index=True)
        df['valid_date'] = pd.to_datetime(df['valid_date']).dt.tz_localize(None)
        df['verification_date'] = pd.to_datetime(df['verification_date']).dt.tz_localize(None)

        logger.info(f'Date range in the data : {min(df['verification_date'])}-{max(df['verification_date'])}')

        df = df.sort_values(by=['mi.number', 'verification_date']).copy()

        df['check'] = 'Периодическая'
        first_check_mask = (df['result_text'] == 'Пригодно') & ~df.duplicated(subset='mi.number', keep='first')
        df.loc[first_check_mask, 'check'] = 'Первичная'

        first_check_date = df[first_check_mask].groupby('mi.number')['verification_date'].min()
        df['station_age'] = (df['verification_date'] - df['mi.number'].map(first_check_date)).dt.days // 365

        df['verification_year'] = df['verification_date'].dt.year

        df['mi.number'].value_counts()

        def rename_mitype(mitype):
            if 'Vantage Pro' in mitype:
                return 'Davis'
            elif 'WXT' in mitype:
                return 'Vaisala'
            elif 'PWS' in mitype:
                return 'ICB'
            elif 'WS-UMB' in mitype:
                return 'Lufft'
            elif 'M-49M' in mitype:
                return 'Сафоновский'
            elif 'СОКОЛ-М1' in mitype:
                return 'СОКОЛ-М1'
            elif any(item in mitype for item in ['ДВН', 'ДВС', 'ДО', 'ДТВ', 'ДД']):
                return 'Минимакс-94'
            elif 'IWS' in mitype:
                return 'Бурстройпроект'
            return mitype

        df['mi.manufacturer'] = df['mi.mitype'].apply(rename_mitype)

        pivot_table = df.pivot_table(
            index=['check', 'mi.manufacturer'], 
            columns='verification_year', 
            values='mi.mitnumber', 
            aggfunc='count', 
            fill_value=0
        )

        # Учитываем множитель 1/4 для категории "Минимакс-94"
        checks = ['Периодическая', 'Первичная']
        for check in checks:
            pivot_table.loc[(check, 'Минимакс-94')] = pivot_table.loc[(check, 'Минимакс-94')] // 4

        pivot_table.to_csv('data/main_pivot.csv', encoding='utf-8')
        all_data.to_csv('data/all_data.csv', index=False, encoding='utf-8')

        upload_date = datetime.datetime.now()
        upload_date_str = upload_date.strftime("%Y-%m-%d")
        # Convert the pivot_table DataFrame to a list of dictionaries
        pivot_table_data = [{'upload_date': upload_date_str, 'data' : pivot_table.to_dict(orient='records')}]

        for record in pivot_table_data[0]['data']:
            for key in list(record.keys()):
                if not isinstance(key, str):
                    # Convert the numeric key to a string
                    record[str(key)] = record.pop(key)

        # Save the data to MongoDB using the MongoDBManager class
        mongo_manager = MongoDBManager(db_host=DB_HOST, db_port=DB_PORT, db_name=DB_NAME)
        mongo_manager.save_data(data=pivot_table_data, table_name=DB_MAIN_TABLE_NAME)


        logger.info('The data was saved in csv.')

    except Exception as e:
        logger.error('Error in run_scraper_and_processor: %s', str(e))

def upload_daemon():
    schedule = Scheduler()
    trigger_time = datetime.time(hour=HOURS_UPLOADING, minute=MINUTES_UPLOADING)
    schedule.daily(timing=trigger_time, handle=run_uploader)
    
    hours_str = str(HOURS_UPLOADING).zfill(2)
    minutes_str = str(MINUTES_UPLOADING).zfill(2)

    logger.info(f"Initializating uploading daemon with daily uploading at {hours_str}:{minutes_str}")

    while True:
        schedule.exec_jobs()
        time.sleep(DAEMON_SLEEPING_TIME)