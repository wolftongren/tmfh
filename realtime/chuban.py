#coding=utf-8

import tushare as ts
import pandas as pd
import pymysql
import time
import datetime
from sqlalchemy import create_engine

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')
sql = "SELECT distinct code, name FROM `stockBasics`"
dfstocks = pd.read_sql(sql, conn)

engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')

t930 = datetime.time(hour=9, minute=25, second=0)
t1130 = datetime.time(hour=11, minute=30, second=10)
t1300 = datetime.time(hour=13, minute=0, second=0)
t1500 = datetime.time(hour=15, minute=0, second=10)

dfChuban = pd.DataFrame(columns=['code', 'name', 'cbTime', 'isBeiza'])
dfBeiza = pd.DataFrame(columns=['code', 'name', 'bzTime', 'zf' 'a1_p'])

while True:

    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()

    if (t > t930 and t < t1130) or (t > t1300 and t > t1500):
        print "fetching data...", datetime.datetime.now()
        dfResult = pd.DataFrame()
        for i in range(0, len(dfstocks) / 500 + 1):
            df = ts.get_realtime_quotes(dfstocks.iloc[i * 500:(i + 1) * 500, 0])
            if df is None:
                pass
            else:
                dfResult = dfResult.append(df)

        r = datetime.datetime.now().strftime("%H:%M:%S")

        dff = dfResult.copy()

        dff['zhangfu'] = 0.0
        dff['chuban'] = 0.0
        dff['zf'] = 0.0
        dff['rtime'] = r
        dff['cbtime'] = 0
        dff['bztime'] = 0

        dff[['price']] = dff[['price']].astype(float)
        dff[['pre_close']] = dff[['pre_close']].astype(float)
        dff[['high']] = dff[['high']].astype(float)
        dff[['low']] = dff[['low']].astype(float)
        dff[['zf']] = dff[['zf']].astype(float)
        dff[['a1_p']] = dff[['a1_p']].astype(float)
        dff[['open']] = dff[['open']].astype(float)

        dff = dff[dff['volume'] > '0']

        dff['zhangfu'] = dff['price'] / dff['pre_close']
        dff['chuban'] = dff['high'] / dff['pre_close']
        dff['zf'] = (dff['price'] / dff['pre_close'] - 1) * 100

        dfMonitor = dff[dff['chuban'] > 1.099]
        dfBeiza = dfMonitor[dfMonitor['zhangfu'] < 1.099]

        for i in range(0, len(dfMonitor)):
            code = dfMonitor.iloc[i]['code']
            name = dfMonitor.iloc[i]['name']
            zf = dfMonitor.iloc[i]['zf']
            time = dfMonitor.iloc[i]['time']
            high = dfMonitor.iloc[i]['high']
            low = dfMonitor.iloc[i]['low']
            chuban = dfMonitor.iloc[i]['chuban']
            zhangfu = dfMonitor.iloc[i]['zhangfu']
            a1_p = dfMonitor.iloc[i]['a1_p']

            dfff = dfChuban[dfChuban['code'] == code]
            if len(dfff):  # already in the chuban list
                pass
            else:  # first time chuban
                s = pd.Series(index=['code', 'name', 'cbTime', 'isBeiza'])
                s[['code']] = s[['code']].astype(str)

                s['code'] = code
                s['name'] = name
                s['cbTime'] = time
                s['isBeiza'] = 0
                dfChuban = dfChuban.append(s, ignore_index=True)
        print "chuban: "
        print dfChuban
        dfChuban.to_sql('rtChubanTime', engine, index=False, if_exists='replace')

        # update how many stocks BeiZa
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')
        c = conn.cursor()
        for i in range(0, len(dfBeiza)):
            code = dfBeiza.iloc[i]['code']
            sql = "update rtChubanTime set isBeiza = 1 where code = %s"
            c.execute(sql, code)
        conn.commit()
        c.close()



