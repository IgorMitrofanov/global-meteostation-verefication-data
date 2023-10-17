import pandas as pd

df_davis = pd.read_excel('data/all_years_VantagePro_Станции.xlsx')
df_vaisala = pd.read_excel('data/all_years_WXT_Метеостанции.xlsx')
df_icb = pd.read_excel('data/all_years_PWS_Метеостанции.xlsx')
df_lufft = pd.read_excel('data/all_years_WSUMB_Станции.xlsx')
df_safonovskiy = pd.read_excel('data/all_years_М-49М_Станции.xlsx')
df_sokol = pd.read_excel('data/all_years_СОКОЛ-М1_Станции.xlsx')

df_all = pd.concat([df_davis, df_vaisala, df_icb, df_lufft, df_safonovskiy, df_sokol])

df_all.to_excel('all_data.xlsx')