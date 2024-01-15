import pandas as pd

from auto.logger import logger

df = pd.read_excel('data/all_data.xlsx', usecols=[
    'mi.mitnumber',
    'mi.modification',
    'mi.number',
    'valid_date',
    'result_docnum',
    'result_text',
    'mi.mitype',
    'mi.mititle',
    'org_title',
    'vri_id',
    'verification_date'
])

df['valid_date'] = pd.to_datetime(df['valid_date']).dt.tz_localize(None)
df['verification_date'] = pd.to_datetime(df['verification_date']).dt.tz_localize(None)

logger.info(min(df['verification_date']), max(df['verification_date']))

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

pivot_table


pivot_table.to_csv('main_pivot.csv')