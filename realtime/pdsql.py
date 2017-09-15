#coding=utf-8


import pandas as pd
import numpy as np
import pymysql
import time
import datetime
import tushare as ts

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')

sql = "select code from stockBasics where industry like '铝' "
dfstocks = pd.read_sql(sql, conn)

d = datetime.datetime.now().date()
t = datetime.datetime.now().time()
print d, t, "running initDB.py"

while True:

    time.sleep(5)

    dff = ts.get_realtime_quotes(dfstocks['code'])

    dff['zhangfu'] = 0.0
    dff[['price']] = dff[['price']].astype(float)
    dff[['pre_close']] = dff[['pre_close']].astype(float)
    dff['zhangfu'] = (dff['price'] / dff['pre_close'] - 1 ) * 100

    print dff[['code', 'name', 'zhangfu']]


