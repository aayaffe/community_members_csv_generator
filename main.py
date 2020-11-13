import json
from collections import namedtuple
from sys import path
import pandas
from gsheets import Sheets
from os import path

configs_file = 'config.json'


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


def get_config(file):

    if not path.isfile(file):
        return None

    with open(file, "r") as f:
        raw_config = f.read()
        return json2obj(raw_config)

sheets = Sheets.from_files('client_secrets.json', 'storage.json')
s = sheets.get(get_config(configs_file).sheet_url)
s.find('רשימת מועדון').to_csv('members_master.csv', encoding='utf-8', dialect='excel')





df = pandas.read_csv('members_master.csv',
                     names=['שם משפחה', 'שם פרטי', 'חולצה', 'סירה', 'ת.ז', 'שם בן/בת הזוג', 'כתובת', 'תאריך לידה',
                            'טלפון', 'טלפון נוסף', 'דואל', 'דואל נוסף',
                            '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021'], encoding='utf8')
df = df.iloc[6:]
df = df.drop(['חולצה', 'ת.ז', 'כתובת', 'תאריך לידה', 'טלפון', 'טלפון נוסף'], axis=1)
years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2025', '2026']
latest_arr = []
total_years_arr = []
for index, row in df.iterrows():
    latest = -1
    total_years = ""
    for y in years:
        try:
            if str(row[y]) and (str(row[y]) != 'nan'):
                latest = y
                if total_years:
                    total_years += "|" + str(y)
                else:
                    total_years = str(y)
        except KeyError:
            continue
    latest_arr.append(latest)
    total_years_arr.append(total_years)
df["Subscription_Years"] = total_years_arr
df["last_year"] = latest_arr
df.to_csv('members_db-1.csv', index=False, header=True)
