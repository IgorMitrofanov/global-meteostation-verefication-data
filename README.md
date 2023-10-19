# global-meteostation-data-parser
 
Задача состоит из нескольких этапов:

1. Парсинг данных сервиса https://fgis.gost.ru/fundmetrology/cm/results по поверке метеостанций различных производителей. Фильтры полей:
   
   1.1 Производитель Davis: Наименование СИ - "Станции", Тип СИ - Vantage Pro;
   
   1.2 Производитель Vaisala: Наименование СИ - "Метеостанции", Тип СИ - WXT;
   
   1.3 Производитель ICB: Наименование СИ - "Метеостанции", Тип СИ - PWS;
   
   1.4 Производитель Lufft: Наименование СИ - "Станции", Тип СИ - WS UMB;
   
   1.5 Производитель Сафоновский: Наименование СИ - "Станции", Тип СИ - М-49М;
   
   1.6 Производитель Сокол-М1: Наименование СИ - "Станции", Тип СИ - СОКОЛ-М1.

   1.7 Производитель Минимакс-94:
   
       1.7.1 Наименование СИ - "Датчики направления ветра", Тип СИ - "ДВН";
   
       1.7.2 Наименование СИ - "Датчики скорости ветра", Тип СИ - "ДВС";
   
       1.7.3 Наименование СИ - "Датчики осадков", Тип СИ - "ДО";
   
       1.7.4 Наименование СИ - "Датчики влажности и температуры грунта", Тип СИ - "ДВГ";
   
       1.7.5 Наименование СИ - "Датчики температуры и влажности воздуха", Тип СИ - "ДТВ";
   
       1.7.6 Наименование СИ - "Датчики атмосферного давления", Тип СИ - "ДД".
   
3. Полученные данные объединить, добавить поля:
   
   2.1 Тип поверки - периодическая или первичная;
   
   2.2 Возраст метеостанции - число целых лет с момента первичной поверки.
   
4. Провести первичный анализ полученных данных.
5. Уточняющий отчет за релевантный период (с 2020 года).

Результаты:
1. Парсер представлен в файле [RST_automatic_parser_to_csv.py](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/RST_automatic_parser_to_csv.py), с гибкой настройков требуемых фильтров;
2. Выгруженные, объединенные и итоговые данные (с требуемыми полями) находятся в каталоге [data](https://github.com/IgorMitrofanov/global-meteostation-data-parser/tree/main/data), скрипт для мерджа данных представлен в файле [data_merging.py](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/data_merging.py);
3. Анализ представлен в файле [analytics.ipynb](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics.ipynb), а так же в файле [analytics.html](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics.html) для презентации.
4. Уточняющий отчет за релевантный период представлен в файле [analytics_from_2020.ipynb](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics_from_2020.ipynb), а так же в файле [analytics_from_2020.html](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics_from_2020.html) для презентации.
