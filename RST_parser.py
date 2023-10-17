import requests
import pandas as pd

# Функция для отправки запроса и получения данных
def get_data(params):
    url = "https://fgis.gost.ru/fundmetrology/cm/xcdb/vri/select"
    response = requests.get(url, params=params)
    data = response.json()
    docs = data['response']['docs']
    df = pd.DataFrame(docs)
    return df


def main():
    page = 0
    year = '*' # * - все года
    modification = 'Сокол-М1'
    filter_value = f'verification_year:{year} AND mi.modification:{modification}'  

    # Создаем пустой DataFrame для сохранения данных
    all_data = pd.DataFrame()

    while True:
        # Создаем параметры запроса
        params = {
            'fq': f'{filter_value}',
            'q': '*',
            'fl': 'vri_id,org_title,mi.mitnumber,mi.mititle,mi.mitype,mi.modification,mi.number,verification_date,valid_date,applicability,result_docnum,sticker_num',
            'sort': 'verification_date desc,org_title asc',
            'rows': 100,
            'start': page * 20
        }

        df = get_data(params)
        # Добавляем полученные данные в общий DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)

        # Выводим данные
        print(df)

        # Запрашиваем у пользователя, хочет ли он продолжить просмотр
        user_input = input("Do you want to load more data (y/n)? ")
        if user_input.lower() != 'y':
            break

        # Увеличиваем страницу
        page += 1
    # Сохраняем все данные в файл Excel
    all_data.to_excel('verification_data.xlsx', index=False, engine='openpyxl')

    
if __name__ == '__main__':
    main()


