# /dashboard/run_app.py

import pandas as pd
import dash_mantine_components as dmc
from dash_express import DashExpress, Page
from dash import html

from constants import SERVER_HOST, SERVER_PORT
from dashboard.build_functions import pie_manufactures, bar_chart_veriffy_manufactures, bar_chart_avg_age, hist_manufacturer_groups, pivot_table, facetgrid_plot_age

get_df_all = lambda: pd.read_csv('data/all_data.csv')

get_df_main_pivot = lambda: pd.read_csv('data/main_pivot.csv')

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


if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT)