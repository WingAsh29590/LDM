import json
from math import fabs

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

file = open('RU.txt', 'r', encoding='utf-8')  # Файл обработанной базы данных (Оставлены только города)
'''
    Перенос базы данных из файла в список
'''
cities_list = []
for line in file:
    cities_list.append(line.split('\t'))

# Словарь временных зон для вычета разницы времени
timezones = {'Europe/Kaliningrad': 0, 'Europe/Moscow': 1, 'Europe/Samara': 2, 'Asia/Yekaterinburg': 3, 'Asia/Omsk': 4,
             'Asia/Krasnoyarsk': 5, 'Asia/Irkutsk': 6, 'Asia/Yakutsk': 7, 'Asia/Vladivostok': 8, 'Asia/Magadan': 9,
             'Asia/Kamchatka': 10}

'''
    Страница /cityInfo, принимает 1 параметр GET: 'geonameid'.
    Поиск искомого города происходит через бинарный поиск.
    Примерное время затраченное на поиск города - 5.2999999999858716e-05
    После обнаружения города он переносится в словарь, который имеет структуру JSON файла
'''


@app.route('/cityInfo', methods=['GET'])
def cityInfo():
    geonameid = int(request.args.get('geonameid'))
    cities_count = 201177
    low = 0
    high = cities_count - 1
    while low <= high:
        mid = (low + high) // 2
        if geonameid < int(cities_list[mid][0]):
            high = mid - 1
        elif geonameid > int(cities_list[mid][0]):
            low = mid + 1
        else:
            city_dict = {'geonameid': cities_list[mid][0], 'name': cities_list[mid][1],
                         'asciiname': cities_list[mid][2], 'alternatenames': cities_list[mid][3],
                         'latitude': cities_list[mid][4], 'longtitude': cities_list[mid][5],
                         'feature_class': cities_list[mid][6], 'feature_code': cities_list[mid][7],
                         'county_code': cities_list[mid][8], 'cc2': cities_list[mid][9],
                         'admin1_code': cities_list[mid][10], 'admin2_code': cities_list[mid][11],
                         'admin3_code': cities_list[mid][12], 'admin4_code': cities_list[mid][13],
                         'population': cities_list[mid][14], 'elevation': cities_list[mid][15],
                         'dem': cities_list[mid][16], 'timezone': cities_list[mid][17],
                         'modification_date': cities_list[mid][18][:-1]}
            return json.dumps(city_dict, ensure_ascii=False)
    else:
        return 'No the number'


'''
    Страница /citiesPage, принимает два параметра GET: 
    'number' - номер страницы, 'cnt' - количество элементов на странице.
    Возвращает cnt количество городова на number странице.
'''


@app.route('/citiesPage', methods=['GET'])
def citiesPage():
    page_number = int(request.args.get('number'))
    cities_page_count = int(request.args.get('cnt'))
    cities_count = 201177
    page_count = cities_count // cities_page_count
    cities_page_list = cities_list[((page_number - 1) * cities_page_count):(page_number * cities_page_count)]
    for i in range(len(cities_page_list)):
        cities_page_list[i] = {'geonameid': cities_page_list[i][0], 'name': cities_page_list[i][1],
                               'asciiname': cities_page_list[i][2], 'alternatenames': cities_page_list[i][3],
                               'latitude': cities_page_list[i][4], 'longtitude': cities_page_list[i][5],
                               'feature_class': cities_page_list[i][6], 'feature_code': cities_page_list[i][7],
                               'county_code': cities_page_list[i][8], 'cc2': cities_page_list[i][9],
                               'admin1_code': cities_page_list[i][10], 'admin2_code': cities_page_list[i][11],
                               'admin3_code': cities_page_list[i][12], 'admin4_code': cities_page_list[i][13],
                               'population': cities_page_list[i][14], 'elevation': cities_page_list[i][15],
                               'dem': cities_page_list[i][16], 'timezone': cities_page_list[i][17],
                               'modification_date': cities_page_list[i][18][:-1]}
    return json.dumps(cities_page_list, ensure_ascii=False)


'''
    Страница /compareCitites, принимает два параметра GET: 'city_1' и 'city_2' - название городов на русском.
    Возвращает информацию о двух городах и отдельным словарем возвращает информацию о сравнении:
    'timezone_average' - разница во времени, 'norther' - содержит название города, который севернее,
    'timezone' - содержит True или False (Находится в одной временной зоне или нет)
'''


@app.route('/compareCities', methods=['GET'])
def compareCities():
    city_name_1 = request.args.get('city_1')
    city_name_2 = request.args.get('city_2')
    find_result = [i for i, value in enumerate(cities_list) if city_name_1 in value[3].split(',')]
    max_population = -1
    for i in find_result:
        if max_population < int(cities_list[int(i)][14]):
            max_population = int(cities_list[int(i)][14])
            city_1 = {'geonameid': cities_list[int(i)][0], 'name': cities_list[int(i)][1],
                      'asciiname': cities_list[int(i)][2], 'alternatenames': cities_list[int(i)][3],
                      'latitude': cities_list[int(i)][4], 'longtitude': cities_list[int(i)][5],
                      'feature_class': cities_list[int(i)][6], 'feature_code': cities_list[int(i)][7],
                      'county_code': cities_list[int(i)][8], 'cc2': cities_list[int(i)][9],
                      'admin1_code': cities_list[int(i)][10], 'admin2_code': cities_list[int(i)][11],
                      'admin3_code': cities_list[int(i)][12], 'admin4_code': cities_list[int(i)][13],
                      'population': cities_list[int(i)][14], 'elevation': cities_list[int(i)][15],
                      'dem': cities_list[int(i)][16], 'timezone': cities_list[int(i)][17],
                      'modification_date': cities_list[int(i)][18][:-1]}
    find_result = [i for i, value in enumerate(cities_list) if city_name_2 in value[3].split(',')]
    max_population = -1
    for i in find_result:
        if max_population < int(cities_list[int(i)][14]):
            max_population = int(cities_list[int(i)][14])
            city_2 = {'geonameid': cities_list[int(i)][0], 'name': cities_list[int(i)][1],
                      'asciiname': cities_list[int(i)][2], 'alternatenames': cities_list[int(i)][3],
                      'latitude': cities_list[int(i)][4], 'longtitude': cities_list[int(i)][5],
                      'feature_class': cities_list[int(i)][6], 'feature_code': cities_list[int(i)][7],
                      'county_code': cities_list[int(i)][8], 'cc2': cities_list[int(i)][9],
                      'admin1_code': cities_list[int(i)][10], 'admin2_code': cities_list[int(i)][11],
                      'admin3_code': cities_list[int(i)][12], 'admin4_code': cities_list[int(i)][13],
                      'population': cities_list[int(i)][14], 'elevation': cities_list[int(i)][15],
                      'dem': cities_list[int(i)][16], 'timezone': cities_list[int(i)][17],
                      'modification_date': cities_list[int(i)][18][:-1]}
    rtrn = [city_1, city_2, {'timezone_average': int(fabs(timezones[city_1['timezone']] - timezones[city_2['timezone']]))}]
    if city_1['latitude'] > city_2['latitude']:
        if city_1['timezone'] == city_2['timezone']:
            rtrn[2].update({'northern': city_name_1, 'timezone': True})
            return json.dumps(rtrn, ensure_ascii=False)
        else:
            rtrn[2].update({'northern': city_name_1, 'timezone': True})
            return json.dumps(rtrn, ensure_ascii=False)
    else:
        if city_1['timezone'] == city_2['timezone']:
            rtrn[2].update({'northern': city_name_2, 'timezone': True})
            return json.dumps(rtrn, ensure_ascii=False)
        else:
            rtrn[2].update({'northern': city_name_2, 'timezone': True})
            return json.dumps(rtrn, ensure_ascii=False)

