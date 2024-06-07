# /daemon.py

from scheduler import Scheduler

from uploader import get_df_by_the_filter
from constants import PARAMETERS_LIST, HOURS_UPLOADING, MINUTES_UPLOADING, DAEMON_SLEEPING_TIME, ENCODING, DATA_DIR
import time
from db.mongodb_manager import MongoDBManager
import datetime
import pandas as pd
from logger import get_logger

logger = get_logger(__name__)


def run_uploader():
    mongo_manager = MongoDBManager()
    try:
        all_data = pd.DataFrame()
        for params in PARAMETERS_LIST:
            logger.info(f'Uploading by the filter: {params['mitype'], params['mititle']}')
            data = get_df_by_the_filter(params['mitype'], params['mititle']) # запись в бд
            df = pd.DataFrame(data)
            all_data = pd.concat([all_data, df], ignore_index=True)
        print(all_data['valid_date'].isna().mean(),  all_data['verification_date'].isna().mean()) # has nan, hasn't nan
        all_data['valid_date'] = pd.to_datetime(all_data['valid_date']) #.dt.tz_localize(None)
        all_data['verification_date'] = pd.to_datetime(all_data['verification_date']) #.dt.tz_localize(None)

        logger.info(f'Date range in the data : {min(all_data['verification_date'])}-{max(all_data['verification_date'])}')

        all_data = all_data.sort_values(by=['mi.number', 'verification_date']).copy()

        all_data['check'] = 'Периодическая'
        first_check_mask = (all_data['result_text'] == 'Пригодно') & ~all_data.duplicated(subset='mi.number', keep='first')
        all_data.loc[first_check_mask, 'check'] = 'Первичная'

        first_check_date = all_data[first_check_mask].groupby('mi.number')['verification_date'].min()
        all_data['station_age'] = (all_data['verification_date'] - all_data['mi.number'].map(first_check_date)).dt.days // 365

        all_data['verification_year'] = all_data['verification_date'].dt.year

        all_data['mi.number'].value_counts()

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

        all_data['mi.manufacturer'] = all_data['mi.mitype'].apply(rename_mitype)

        mongo_manager.save_data(data=all_data.to_dict("records"), table_name="all_data")

        pivot_table = all_data.pivot_table(
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

        pivot_table_dict = pivot_table.to_dict('records')

        new_structure = {}

        for entry in pivot_table_dict:
            key = f"{entry['check']}-{entry['mi.manufacturer']}"
            entry.pop('check')
            entry.pop('mi.manufacturer')
            new_structure[key] = {str(k): v for k, v in entry.items()}

        mongo_manager.save_data(data=new_structure, table_name="main_pivot")

        logger.info('The all data was saved and main pivot saved to mongodb.')

    except Exception as e:
        logger.error('Error in run_scraper_and_processor: %s', str(e))

def run_upload_daemon():
    schedule = Scheduler()
    trigger_time = datetime.time(hour=HOURS_UPLOADING, minute=MINUTES_UPLOADING)
    schedule.daily(timing=trigger_time, handle=run_uploader)
    
    hours_str = str(HOURS_UPLOADING).zfill(2)
    minutes_str = str(MINUTES_UPLOADING).zfill(2)

    logger.info(f"Initializating uploading daemon with daily uploading at {hours_str}:{minutes_str}")

    while True:
        schedule.exec_jobs()
        time.sleep(DAEMON_SLEEPING_TIME)