import json
import random
import xlrd
import pandas as pd
from detail_spider import load_index

movie_names = set([])
for sheet_name in pd.ExcelFile('D:/all_index.xlsx').sheet_names[1:]:
    index = pd.ExcelFile('D:/all_index.xlsx').parse(sheet_name, header=None)
    for i in range(index.shape[0]):
        movie_names.add(index.at[i, 0])

temp_all_index = []
all_index, index_point = load_index()
for item in all_index:
    if item['name'] in movie_names:
        temp_all_index.append(item)

movies = [pd.ExcelFile('D:/2011-2015.xlsx').parse('Sheet1'), pd.ExcelFile('D:/2016-1.xlsx').parse('Sheet1'),
          pd.ExcelFile('D:/2016-2.xlsx').parse('Sheet1'), pd.ExcelFile('D:/2017-1.xlsx').parse('Sheet1')]

current = ''
dates = {}
for movie in movies:
    for i in range(movie.shape[0]):
        if current != movie.at[i, '电影名称']:
            current = movie.at[i, '电影名称']
            dates[current] = [{'date': movie.at[i, '时间'], 'sales': movie.at[i, '当日票房（万元）'] * 10000}]
        else:
            dates[current].append({'date': movie.at[i, '时间'], 'sales': movie.at[i, '当日票房（万元）'] * 10000})

names = set(list(dates))

new_all_index = []
for item in temp_all_index:
    if item['name'] in names:
        nitem = item
        nitem['final_date'] = dates[item['name']][0]['date'].__str__()
        print ("{}-{}".format(item['name'], dates[item['name']][0]['date'].__str__()))
        new_all_index.append(item)

with open("all_index.txt", "w") as index_file:
    random.shuffle(temp_all_index)
    print("共计：{}部电影".format(len(temp_all_index)))
    json.dump({'current_in': 0, 'data': temp_all_index}, index_file)
