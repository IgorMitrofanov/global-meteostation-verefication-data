import pandas as pd
import plotly.graph_objects as go
import dash_mantine_components as dmc

from dash_express import DashExpress, Page

get_df_all = lambda: pd.read_csv('data/all_data.csv')

app = DashExpress(logo='Veriffy data dashborad', default_cache_timeout=10)

# Создаем страницу дашборда
page = Page(
    app=app,                    # DashExpress app
    url_path='/',               # Путь страницы
    name='Overview',            # Название страницы
    get_df=get_df_all,              # Функция получения дашборда
    )




####

# def create_pie_chart(data, labels, title):
#     plt.figure(figsize=(8, 8))
#     plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
#     plt.title(title)
#     plt.axis('equal')
#     plt.show()

# def create_bar_chart(data, title, xlabel, ylabel, stacked=False):
#     data.plot(kind='bar', stacked=stacked)
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.show()

# def create_heatmap(data, title, xlabel, ylabel, annot=True, fmt='.1f', cmap='YlGnBu'):
#     sns.heatmap(data, annot=annot, fmt=fmt, cmap=cmap)
#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.show()


# def create_histogram(data, title, xlabel, ylabel):
#     plt.figure(figsize=(12, 8))
#     handles = []  # Список для хранения элементов легенды

#     for label, group_data in data:
#         if label == 'СОКОЛ-М1':
#             alpha = 0.9
#         else:
#             alpha = 0.7
#         if label == "Минимакс-94":
#             scale_factor = 0.25 # Далее по тексту есть причина такого масштабирования
#             heights, bins, _ = plt.hist(group_data['verification_date'], bins=40, visible=False)
#             heights = [h * scale_factor for h in heights]
#             bar_color = 'purple'
#             bar = plt.bar(bins[:-1], heights, width=(bins[1] - bins[0]), alpha=alpha, color=bar_color)
#             handles.append(Line2D([0], [0], color=bar_color, lw=2, label=label))
#         else:
#             hist = plt.hist(group_data['verification_date'], bins=40, alpha=alpha, label=label)
#             handles.append(Line2D([0], [0], color=hist[2][0].get_facecolor(), lw=2, label=label))

#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.legend(handles=handles)  # Добавляем список элементов легенды
#     plt.show()




# mi_type_avg_station_age = df.groupby('mi.manufacturer')['station_age'].mean()
# create_bar_chart(
#     mi_type_avg_station_age, 
#     'Средний возраст метеостанции (СИ) каждого производителя', 
#     'Производитель', 
#     'Средний возраст станции, лет'
#     )

# g = sns.FacetGrid(df, col="mi.manufacturer", height=4, col_wrap=4)
# g.map(plt.hist, 'station_age', bins=10)
# g.set_axis_labels('Возраст станции', 'Количество записей')
# plt.suptitle('Распределение возраста метеостанций (СИ) для каждого производителя', y=1.02)
# plt.show()

# mi_type_check_result_counts = df.groupby(['mi.manufacturer', 'check', 'result_text']).size().unstack().fillna(0)

# # Учитываем множитель 1/4 для категории "Минимакс-94"
# checks = ['Периодическая', 'Первичная']
# for check in checks:
#     mi_type_check_result_counts.loc[('Минимакс-94', check), 
#                                     'Непригодно'] = mi_type_check_result_counts.loc[('Минимакс-94', check), 'Непригодно'] // 4
#     mi_type_check_result_counts.loc[('Минимакс-94', check), 
#                                     'Пригодно'] = mi_type_check_result_counts.loc[('Минимакс-94', check), 'Пригодно'] // 4

# create_heatmap(
#     mi_type_check_result_counts, 
#     'Число поверок каждого производителя с разбивкой по типу и результату поверки, шт', 
#     'Поверка', 
#     'Производитель')

# mi_type_check_result_percentages = mi_type_check_result_counts.div(mi_type_check_result_counts.sum(axis=1), axis=0) * 100
# create_heatmap(
#     mi_type_check_result_percentages, 
#     'Доля поверок каждого производителя с разбивкой по типу и результату поверки, %', 
#     'Поверка', 
#     'Производитель')

# manufacturer_groups = df.groupby('mi.manufacturer')
# create_histogram(
#     manufacturer_groups, 
#     'Гистограмма дат поверок для каждого производителя', 
#     'Дата поверки', 
#     'Частота'
# )

# manufacturer_groups_primary = df[df['check'] == 'Первичная'].groupby('mi.manufacturer')
# create_histogram(
#     manufacturer_groups_primary,
#       'Гистограмма дат первичной поверки для каждого производителя', 
#       'Дата первичной поверки', 
#       'Частота'
# )

# pivot_table = df.pivot_table(
#     index=['check', 'mi.manufacturer'], 
#     columns='verification_year', 
#     values='mi.mitnumber', 
#     aggfunc='count', 
#     fill_value=0
# )

# # Учитываем множитель 1/4 для категории "Минимакс-94"
# checks = ['Периодическая', 'Первичная']
# for check in checks:
#     pivot_table.loc[(check, 'Минимакс-94')] = pivot_table.loc[(check, 'Минимакс-94')] // 4

# pivot_table

####

# Функция построения графика
def pie_func_all(df):
    mi_type_counts = df['mi.manufacturer'].value_counts()

    # Учитываем деление на 4 только для "Минимакс-94"
    if 'Минимакс-94' in mi_type_counts.index:
        mi_type_counts['Минимакс-94'] /= 4


    fig = go.Figure(data=[go.Pie(labels=mi_type_counts.index, values=mi_type_counts, textinfo='percent+label')])
    fig.update_layout(title_text='Доля производителей метеостанций (СИ), проходящих поверку')
    return fig

# def pie_func_minimax(df):
#     mi_type_counts = df[df['mi.manufacturer'] == 'Минимакс-94']['mi.mititle'].value_counts()
#     fig = go.Figure(data=[go.Pie(labels=mi_type_counts.index, values=mi_type_counts, textinfo='percent+label')])
#     fig.update_layout(title_text='Доля поверямых средств измерений производителя Минимакс-94')
#     return fig


def create_bar_chart(df):
    mi_type_check_counts = df.groupby(['mi.manufacturer', 'check']).size().unstack()
    
    # mi_type_check_counts.loc['Минимакс-94'] = mi_type_check_counts.loc['Минимакс-94'] / 4 # Учитываем вышесказанное
    # Create traces for each bar
    bars = []
    for label, group_data in mi_type_check_counts.iterrows():
        print(label)
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

# mi_type_avg_station_age = df.groupby('mi.manufacturer')['station_age'].mean()
# create_bar_chart(
#     mi_type_avg_station_age, 
#     'Средний возраст метеостанции (СИ) каждого производителя', 
#     'Производитель', 
#     'Средний возраст станции, лет'
#     )

# Размечаем макет
page.layout = dmc.SimpleGrid(children=[
    page.add_graph(render_func=pie_func_all), 
    page.add_graph(render_func=create_bar_chart), 
    page.add_graph(render_func=create_bar_chart_avg_age)], 
    cols=2
)

# , page.add_graph(render_func=create_bar_chart)

# По каким колонкам фильтруем
page.add_autofilter('mi.manufacturer', multi=True)
page.add_autofilter('mi.mitype', multi=True)
page.add_autofilter('mi.mititle', multi=True)
page.add_autofilter('check', multi=True)
app.run(host="192.168.54.86")