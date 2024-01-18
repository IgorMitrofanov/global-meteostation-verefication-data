# /dashboard/functions.py

import plotly.graph_objects as go
from dash.dash_table import DataTable
from plotly.subplots import make_subplots

def pie_manufactures(df):
    mi_type_counts = df['mi.manufacturer'].value_counts()

    mi_type_counts = mi_type_counts.astype(float)
    # Учитываем деление на 4 только для "Минимакс-94"
    if 'Минимакс-94' in mi_type_counts.index:
        mi_type_counts['Минимакс-94'] = mi_type_counts['Минимакс-94'] / 4

    fig = go.Figure(data=[go.Pie(labels=mi_type_counts.index, values=mi_type_counts, textinfo='percent+label')])
    fig.update_layout(title_text='Доля производителей метеостанций (СИ), проходящих поверку')

    return fig

def bar_chart_veriffy_manufactures(df):
    mi_type_check_counts = df.groupby(['mi.manufacturer', 'check']).size().unstack()
    
    bars = []
    for label, group_data in mi_type_check_counts.iterrows():
        if label == 'Минимакс-94':
            group_data /= 4
        group_data = group_data.astype(int)

        bar = go.Bar(x=group_data.index, y=group_data.values, name=label)
        bars.append(bar)

    # Create layout
    layout = go.Layout(
        title='Количество проверок метeостанций',
        xaxis=dict(title='Производитель'),
        yaxis=dict(title='Количество записей'),
    )

    # Create figure
    fig = go.Figure(data=bars, layout=layout)
    return fig

def bar_chart_avg_age(df):

    df = df.query('check == "Периодическая"').copy()
    mi_type_avg_station_age = df.groupby('mi.manufacturer')['station_age'].mean()

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

def hist_manufacturer_groups(df):
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

def pivot_table(df):
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

def facetgrid_plot_age(df):
    manufacturer_list = df['mi.manufacturer'].unique()
    num_manufacturers = len(manufacturer_list)
    
    fig = make_subplots(rows=num_manufacturers, cols=1, subplot_titles=manufacturer_list)
    
    for i, manufacturer in enumerate(manufacturer_list, start=1):
        data_subset = df[df['mi.manufacturer'] == manufacturer]
        
        # Explicitly set bin edges to avoid negative values
        bin_edges = list(range(int(data_subset['station_age'].min()), int(data_subset['station_age'].max()) + 2))

        hist_trace = go.Histogram(x=data_subset['station_age'], name=manufacturer, opacity=0.9, xbins=dict(start=min(bin_edges), end=max(bin_edges), size=1))
        fig.add_trace(hist_trace, row=i, col=1)
    
        fig.update_yaxes(title_text='Количество записей', row=i, col=1)
    
    fig.update_xaxes(title_text='Возраст станции', row=num_manufacturers, col=1)
    
    fig.update_layout(
        title_text='Распределение возраста метеостанций (СИ) для каждого производителя',
        height=num_manufacturers * 300,
        showlegend=False,
        xaxis_range=[0, None]  # Ensure x-axis starts from 0
    )
    
    return fig
