# Глобальная база по поверке метеостанций

## RU

### Цель проекта

Этот проект включает в себя несколько этапов:

1. **Парсинг данных** с сервиса [fgis.gost.ru](https://fgis.gost.ru/fundmetrology/cm/results) о калибровке метеостанций различных производителей. Данные должны быть отфильтрованы на основе следующих критериев:
   
   1.1 Производитель Davis: Наименование СИ - "Станции", Тип СИ - Vantage Pro;
   
   1.2 Производитель Vaisala: Наименование СИ - "Метеостанции", Тип СИ - WXT;
   
   1.3 Производитель ICB: Наименование СИ - "Метеостанции", Тип СИ - PWS;
   
   1.4 Производитель Lufft: Наименование СИ - "Станции", Тип СИ - WS UMB;
   
   1.5 Производитель Сафоновский: Наименование СИ - "Станции", Тип СИ - М-49М;
   
   1.6 Производитель Сокол-М1: Наименование СИ - "Станции", Тип СИ - СОКОЛ-М1;

   1.7 Производитель Минимакс-94: Наименование СИ - "Датчики направления ветра", "Датчики скорости ветра", "Датчики осадков", "Датчики влажности и температуры грунта", "Датчики температуры и влажности воздуха", "Датчики атмосферного давления", Тип СИ "ДВН", "ДВС", "ДО", "ДВГ", "ДТВ", "ДД" соответственно.

3. **Обработка данных**: Объединение спарсенных данных и добавление следующих полей:
   
   2.1 Тип поверки - периодическая или первичная;
   
   2.2 Возраст метеостанции - число целых лет с момента первичной поверки.

4. **Исходный анализ данных**.

5. **Подробный отчет за актуальный период** (начиная с 2020 года).

Результаты:
1. Парсер представлен в файле [RST_automatic_parser_to_csv.py](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/RST_automatic_parser_to_csv.py), с гибкими фильтрами для соответствия указанным критериям.
2. Извлеченные, объединенные и окончательные данные (с необходимыми полями) находятся в каталоге [data](https://github.com/IgorMitrofanov/global-meteostation-data-parser/tree/main/data). Скрипт для объединения данных представлен в файле [data_merging.py](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/data_merging.py).
3. Анализ данных представлен в файле [analytics.ipynb](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics.ipynb) и также в [analytics.html](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics.html) для презентационных целей.
4. Подробный отчет за актуальный период доступен в файле [analytics_from_2020.ipynb](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics_from_2020.ipynb) и также в [analytics_from_2020.html](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics_from_2020.html) для презентации.

**Контактная информация:**
- Telegram: @igor_mtrfnv
- Email: i.v.mitrofanov@ya.ru

# Global Meteostation Verification Data

## EN

### Project Objective

This project consists of several stages:

1. **Data Parsing** from the [fgis.gost.ru](https://fgis.gost.ru/fundmetrology/cm/results) service regarding the calibration of meteorological stations from various manufacturers. The data should be filtered based on the following criteria:

   1.1 Manufacturer Davis: Name of SI - "Stations," SI Type - Vantage Pro;

   1.2 Manufacturer Vaisala: Name of SI - "Meteorological Stations," SI Type - WXT;

   1.3 Manufacturer ICB: Name of SI - "Meteorological Stations," SI Type - PWS;

   1.4 Manufacturer Lufft: Name of SI - "Stations," SI Type - WS UMB;

   1.5 Manufacturer Safonovskiy: Name of SI - "Stations," SI Type - М-49М;

   1.6 Manufacturer Sokol-M1: Name of SI - "Stations," SI Type - СОКОЛ-М1;

   1.7 Manufacturer Minimax-94: Name of SI - "Wind Direction Sensors," "Wind Speed Sensors," "Precipitation Sensors," "Soil Humidity and Temperature Sensors," "Air Temperature and Humidity Sensors," "Atmospheric Pressure Sensors," SI Type "WDS," "WSS," "PS," "SH&TS," "ATHS," "APS," respectively.

3. **Data Processing**: Combine the parsed data and add the following fields:

   2.1 Verification Type - periodic or primary;

   2.2 Age of the meteorological station - the number of whole years since the primary verification.

4. **Initial Data Analysis**.

5. **Detailed Report for the Current Period** (starting from 2020).

Results:
1. The parser is provided in the file [RST_automatic_parser_to_csv.py](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/RST_automatic_parser_to_csv.py), with flexible filters to match the specified criteria.
2. Extracted, merged, and finalized data (with the necessary fields) can be found in the [data](https://github.com/IgorMitrofanov/global-meteostation-data-parser/tree/main/data) directory. The script for data merging is in the file [data_merging.py](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/data_merging.py).
3. Data analysis is presented in the file [analytics.ipynb](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics.ipynb) and also in [analytics.html](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics.html) for presentation purposes.
4. A detailed report for the current period is available in the file [analytics_from_2020.ipynb](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics_from_2020.ipynb) and also in [analytics_from_2020.html](https://github.com/IgorMitrofanov/global-meteostation-data-parser/blob/main/analytics_from_2020.html) for presentation.

**Contact Information:**
- Telegram: @igor_mtrfnv
- Email: i.v.mitrofanov@ya.ru

