import pandas as pd

df_davis = pd.read_excel('data/all_years_VantagePro_Станции.xlsx')
df_vaisala = pd.read_excel('data/all_years_WXT_Метеостанции.xlsx')
df_icb = pd.read_excel('data/all_years_PWS_Метеостанции.xlsx')
df_lufft = pd.read_excel('data/all_years_WSUMB_Станции.xlsx')
df_safonovskiy = pd.read_excel('data/all_years_М-49М_Станции.xlsx')
df_sokol = pd.read_excel('data/all_years_СОКОЛ-М1_Станции.xlsx')

# Минимакс-94
df_dvn = pd.read_excel('data/all_years_ДВН_Датчикинаправленияветра.xlsx')
df_dvs = pd.read_excel('data/all_years_ДВС_Датчикискоростиветра.xlsx')
df_dd = pd.read_excel('data/all_years_ДД_Датчикиатмосферногодавления.xlsx')
df_do = pd.read_excel('data/all_years_ДО_Датчикиосадков.xlsx')
df_dtv = pd.read_excel('data/all_years_ДТВ_Датчикитемпературыивлажностивоздуха.xlsx')

df_minimax = pd.concat([df_dvn, df_dvs, df_dd, df_do, df_dtv])

df_burstroy = pd.read_excel('data/all_years_IWS_Датчикикомплексныепараметроватмосферы.xlsx')

df_all = pd.concat([df_davis, df_vaisala, df_icb, df_lufft, df_safonovskiy, df_sokol, df_minimax, df_burstroy])

df_all.to_excel('data/all_data.xlsx', index=False)