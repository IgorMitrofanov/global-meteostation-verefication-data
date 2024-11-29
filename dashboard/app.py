# /dashboard/app.py

import pandas as pd
import dash_mantine_components as dmc
from dash_express import DashExpress, Page
from dash import html

from dashboard.build_functions import pie_manufactures, bar_chart_veriffy_manufactures, bar_chart_avg_age, hist_manufacturer_groups, pivot_table, facetgrid_plot_age

# app.run(host="192.168.54.86")

def run_dashboard_app():

    get_df_all = lambda: pd.read_csv('data/all_data.csv') # заменить на БД метод

    get_df_main_pivot = lambda: pd.read_csv('data/main_pivot.csv') # заменить на БД метод

    app = DashExpress(logo='Витрина данных по поверке СИ', default_cache_timeout=10)

    # Создаем страницу дашборда
    page_visual = Page(
        app=app,
        url_path='/', 
        name='Общая информация по поверкам',
        get_df=get_df_all,
        )

    page_pivot = Page(
        app=app,                   
        url_path='/pivot',             
        name='Сводная таблица',          
        get_df=get_df_main_pivot,              
        )

    page_lifetime = Page(
        app=app,                   
        url_path='/lifetime',             
        name='Время жизни СИ',          
        get_df=get_df_all,              
        )
        

    # Размечаем макет
    page_visual.layout = dmc.SimpleGrid(children=[
        page_visual.add_graph(render_func=pie_manufactures), 
        page_visual.add_graph(render_func=bar_chart_veriffy_manufactures), 
        page_visual.add_graph(render_func=bar_chart_avg_age),
        page_visual.add_graph(render_func=hist_manufacturer_groups),
        ], 
        cols=2
    )


    page_pivot.layout = dmc.SimpleGrid(children=[
        html.Div([pivot_table(get_df_main_pivot())])]
    )


    page_lifetime.layout = dmc.SimpleGrid(children=[
        page_lifetime.add_graph(render_func=facetgrid_plot_age)]
    )


    # По каким колонкам фильтруем
    page_visual.add_autofilter('mi.manufacturer', multi=True, label='Производитель')
    page_visual.add_autofilter('mi.mitype', multi=True, label='Тип СИ')
    page_visual.add_autofilter('mi.mititle', multi=True, label='Наименование СИ')
    page_visual.add_autofilter('check', multi=True, label='Тип поверки')
    page_visual.add_autofilter('verification_year', multi=True, label='Год поверки', type='select')
    
    app.run(host="0.0.0.0", port="8080") # здесь будет имя хоста из env var
