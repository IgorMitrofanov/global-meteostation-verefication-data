import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc
import matplotlib.pyplot as plt

from dash_express import DashExpress, Page

get_df_all = lambda: pd.read_csv('data/all_data.csv')

get_df_main_pivot = lambda: pd.read_csv('data/main_pivot.csv')

app = DashExpress(logo='Витрина данных по поверке СИ', default_cache_timeout=10)

# Создаем страницу дашборда
page_visual = Page(
    app=app,                    # DashExpress app
    url_path='/',               # Путь страницы
    name='Визуализация',            # Название страницы
    get_df=get_df_all,              # Функция получения дашборда
    )

page_pivot = Page(
    app=app,                   
    url_path='/pivot',             
    name='Сводная таблица',          
    get_df=get_df_main_pivot,              
    )

# Функция построения графика
def pie_func_all(df):
    mi_type_counts = df['mi.manufacturer'].value_counts()

    # Учитываем деление на 4 только для "Минимакс-94"
    if 'Минимакс-94' in mi_type_counts.index:
        mi_type_counts['Минимакс-94'] /= 4


    fig = go.Figure(data=[go.Pie(labels=mi_type_counts.index, values=mi_type_counts, textinfo='percent+label')])
    fig.update_layout(title_text='Доля производителей метеостанций (СИ), проходящих поверку')
    return fig


def create_bar_chart(df):
    mi_type_check_counts = df.groupby(['mi.manufacturer', 'check']).size().unstack()
    
    # mi_type_check_counts.loc['Минимакс-94'] = mi_type_check_counts.loc['Минимакс-94'] / 4 # Учитываем вышесказанное
    # Create traces for each bar
    bars = []
    for label, group_data in mi_type_check_counts.iterrows():
        if label == 'Минимакс-94':
            group_data /= 4
        bar = go.Bar(x=group_data.index, y=group_data.values, name=label)
        bars.append(bar)

    # Create layout
    layout = go.Layout(
        title='Количество проверок метеостанций (СИ) с разбивкой по типу поверки',
        xaxis=dict(title='Производитель'),
        yaxis=dict(title='Количество записей'),
       # barmode='stack'
    )

    # Create figure
    fig = go.Figure(data=bars, layout=layout)
    return fig

def create_bar_chart_avg_age(df):
    mi_type_avg_station_age = df.groupby('mi.manufacturer')['station_age'].mean()
    
    # mi_type_check_counts.loc['Минимакс-94'] = mi_type_check_counts.loc['Минимакс-94'] / 4 # Учитываем вышесказанное
    # Create traces for each bar

    bar = go.Bar(x=mi_type_avg_station_age.index, y=mi_type_avg_station_age.values)


    # Create layout
    layout = go.Layout(
        title='Средний возраст метеостанции (СИ) каждого производителя',
        xaxis=dict(title='Производитель'),
        yaxis=dict(title='Средний возраст СИ'),
       # barmode='stack'
    )

    # Create figure
    fig = go.Figure(data=bar, layout=layout)
    return fig

def create_hist_manufacturer_groups(df):
    manufacturer_groups_primary = df[df['check'] == 'Первичная'].groupby('mi.manufacturer')

    fig = go.Figure()

    for label, group_data in manufacturer_groups_primary:
        alpha = 0.6 if label == 'СОКОЛ-М1' else 0.5

        # Уменьшаем количество для 'Минимакс-94'
        if label == 'Минимакс-94':
            group_data['verification_date'] = group_data['verification_date'].sample(frac=0.25)

        fig.add_trace(go.Histogram(x=group_data['verification_date'], name=label, opacity=alpha))

    fig.update_layout(
        title='Гистограмма дат первичной поверки для каждого производителя',
        xaxis_title='Дата первичной поверки',
        yaxis_title='Количество записей',
        barmode='overlay', 
    )

    return fig
    

# Размечаем макет
page_visual.layout = dmc.SimpleGrid(children=[
    page_visual.add_graph(render_func=pie_func_all), 
    page_visual.add_graph(render_func=create_bar_chart), 
    page_visual.add_graph(render_func=create_bar_chart_avg_age),
    page_visual.add_graph(render_func=create_hist_manufacturer_groups),
    ], 
    cols=2
)

from dash import html
from dash_table import DataTable

def create_data_table(df):
    table = DataTable(
        id='pivot-table',
        columns=[
            {'name': col, 'id': col} for col in df.columns
        ],
        data=df.to_dict('records'),
        style_data={
            'color': 'rgb(116, 143, 251)',
            'backgroundColor': 'rgb(26, 27, 30)',
            'fontWeight': 'bold'
            },
        style_header={
            'backgroundColor': 'black',
            'color': 'rgb(116, 143, 251)',
            'fontWeight': 'bold'}
        )
    return table



page_pivot.layout = dmc.SimpleGrid(children=[
    html.Div([create_data_table(get_df_main_pivot())])]
)

# По каким колонкам фильтруем
page_visual.add_autofilter('mi.manufacturer', multi=True, label='Производитель')
page_visual.add_autofilter('mi.mitype', multi=True, label='Тип СИ')
page_visual.add_autofilter('mi.mititle', multi=True, label='Наименование СИ')
page_visual.add_autofilter('check', multi=True, label='Тип поверки')
app.run(host="192.168.54.86")