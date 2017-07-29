#coding=utf-8

import tushare as ts
import pandas as pd
import pymysql
import time
import datetime
from sqlalchemy import create_engine

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stockdata', charset='utf8')
sql = "SELECT distinct code, name FROM `basics`"
dfstocks = pd.read_sql(sql, conn)

engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/falcon?charset=utf8')

t930 = datetime.time(hour=9, minute=30, second=0)
t1130 = datetime.time(hour=11, minute=30, second=10)
t1300 = datetime.time(hour=13, minute=0, second=0)
t1500 = datetime.time(hour=15, minute=0, second=10)

while True:

    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()

    print "sleeping 5s.."
    time.sleep(5)

    if (t > t930 and t < t1130) or (t > t1300 and t < t1500):

        print "fetching data...", datetime.datetime.now()
        dfResult = pd.DataFrame()
        for i in range(0, len(dfstocks)/500+1):
            df = ts.get_realtime_quotes(dfstocks.iloc[i*500:(i+1)*500,0])
            if df is None:
                pass
            else:
                dfResult = dfResult.append(df)

        dff = dfResult.copy()

        dff['zhangfu'] = 0.0
        dff['chuban'] = 0.0
        dff['zf']=0.0
        dff['rtime']= datetime.datetime.now().strftime("%H:%M:%S")


        dff = dff[dff['volume']>'0']

        dff[['price']] = dff[['price']].astype(float)
        dff[['pre_close']] = dff[['pre_close']].astype(float)
        dff[['high']] = dff[['high']].astype(float)
        dff[['low']] = dff[['low']].astype(float)
        dff[['zf']] = dff[['zf']].astype(float)
        dff[['a1_p']] = dff[['a1_p']].astype(float)
        dff[['open']] = dff[['open']].astype(float)

        dff['zhangfu'] =  dff['price'] / dff['pre_close']
        dff['chuban'] = dff['high'] / dff['pre_close']
        dff['zf'] = (dff['price'] / dff['pre_close'] - 1) * 100

        dffshoufa = dff[dff['chuban']>1.4]
        print "shoufa: ", len(dffshoufa)

        dff = dff[dff['chuban']>1.099]
        print "before chuban.................: ", len(dff)
        dffchuban = dff[dff['chuban']<1.4]
        print "after chuban..................: ", len(dffchuban)


        #print dffchuban[['code', 'name', 'zf', 'a1_v']]
        print "jinri zhangting chuban: ", len(dffchuban)
        #print dffchuban['name']
        dffchuban.to_sql('chuban', engine, index=False, if_exists='append')

        dffyizizhangting = dffchuban[dffchuban['low'] == dffchuban['high']]
        dffzhengchang = dffchuban[dffchuban['low'] != dffchuban['high']]
       # print dffzhengchang['name']
        #print dffyizikaipan[['code', 'name', 'zf']]

        dffyizizhangting = dffyizizhangting.append(dffshoufa)
        print "yizi zhangting......", len(dffyizizhangting)
        dffyizizhangting.to_sql('yizi', engine, index=False, if_exists='append')

        dffzhangting = dffzhengchang[dffzhengchang['a1_p']==0]
        print "zhengchang zhangting liebiao......", len(dffzhangting)
        print dffzhangting['name']
        dffzhangting.to_sql('zhengchang', engine, index=False, if_exists='append')

        dffbeiza = dffzhengchang[dffzhengchang['a1_p'] > 0 ]
        print "zhangting beiza liebiao......", len(dffbeiza)
        dffbeiza.to_sql('beiza', engine, index=False, if_exists='append')

    else:
        continue






