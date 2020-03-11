#!/usr/bin/env python
# coding: utf-8

# # Verodata kikkailut


import pandas as pd
import numpy as np
import requests
from json.decoder import JSONDecodeError


## COMBINE CSV FILES

df = pd.read_csv('yhteiso_tuloverotus_julk_20{}.csv'.format(11), delimiter=';',encoding = "ISO-8859-1",
                decimal=',')
df.columns = df.columns.str.split('|', expand=True).droplevel(1).str.strip(' ')



for i in range(12, 19):
    df_t = pd.read_csv('yhteiso_tuloverotus_julk_20{}.csv'.format(i), delimiter=';',encoding = "ISO-8859-1",
                decimal=',')
    df_t.columns = df.columns

    df = df.append(df_t)
    

df.to_csv('verodata.csv')


# SCRAPE RECORDS AND DUMP TO ANNUAL CSV
records = pd.DataFrame()

i = 1500000
while i < 3000000:
    print('Trying: {}'.format(i))
    url = 'https://avoindata.prh.fi/tr/v1/publicnotices?totalResults=false&maxResults=1000' +         '&noticeRegistrationFrom=2011-01-01&noticeRegistrationTo=2018-12-31' +         '&resultsFrom={}'.format(i)
    r = requests.get(url)
    if r.status_code == 429:
        print('status 429')
        print('dumping to csv')
        records.to_csv('recs{}.csv'.format(i))
        break
    else:
        try:
            recs = r.json()['results']
            records = records.append(pd.DataFrame.from_records(recs).iloc[:,[0,1,2,3,5]])
            i += 1000
            if i % 100000 == 0:
                print('dumping to csv')
                records.to_csv('recs{}.csv'.format(i))
                records = pd.DataFrame()
        except JSONDecodeError:
            print('jsondecodeerror')
            continue

import glob
import pandas as pd
import numpy as np

## PROCESS RECORD CSVS
# get data file names
path='C:/Users/lauri/koodi/vero'
filenames = glob.glob(path + "/recs*.csv")
print(filenames)
dfs = []

for filename in filenames:    
    dfs.append(pd.read_csv(filename, index_col=0))

records = pd.concat(dfs, ignore_index=True)

#process records
records.entryCodes = [eval(val) for val in records.entryCodes]
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
records = records.join(pd.DataFrame(mlb.fit_transform(records.entryCodes), 
                                    columns=mlb.classes_, index=records.index))
records.set_index('recordNumber', inplace=True)

mask = records.iloc[:,4:].columns[records.iloc[:,4:].sum() < 100]
records['MUUMUU'] = records[mask].sum(1)
records = records.drop(mask, 1)
records.to_csv('records_processed.csv')


## SCRAPE PROTESTS

from bs4 import BeautifulSoup
import unicodedata
df = pd.DataFrame()
for i in range(1, 10000):
    url = 'http://www.protestilista.com/?page={}'.format(i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    ids = [a['href'][7:] for a in soup.select('a[class=""]')]
    info = [a.text.strip() for a in soup.select('span[class="color-white-mute"]')]
    debtors = info[::3]
    sums = info[1::3]
    dates = info[2::3]
    df = df.append(pd.DataFrame([ids, debtors, sums, dates]).T)
    print('Got ', i)
    if i % 1000 == 0:
        df.to_csv('protestit2_{}.csv'.format(i))

