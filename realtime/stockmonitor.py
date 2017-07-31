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

sql = "select * from `histZhangtingStock`"
dfZhangtingHistory = pd.read_sql(sql, conn)

engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')

t930 = datetime.time(hour=9, minute=30, second=0)
t1130 = datetime.time(hour=11, minute=30, second=10)
t1300 = datetime.time(hour=13, minute=0, second=0)
t1500 = datetime.time(hour=15, minute=0, second=10)

while True:

    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()

    print "sleeping 5s.."
    time.sleep(5)

    if (t > t930 and t < t1130) or (t > t1300 and t > t1500):

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

##########################Zhang Die Ping##############################
        shangzhang = len(dff[dff['zhangfu'] > 1])
        xiadie = len(dff[dff['zhangfu'] < 1])
        pingpan = len(dff[dff['zhangfu'] == 1])
        sql = "insert into rtZhangDiePing(date, time, shangzhang, xiadie, pingpan) values (%s, %s, %s, %s, %s)"
        c = conn.cursor()
        c.execute(sql, (d, t, shangzhang, xiadie, pingpan))
        conn.commit()
        c.close()


##########################ZhangTing Tishi##############################
        dfMonitor = dff[dff['zhangfu'] > 1.080]
        dfMonitor = dfMonitor[dfMonitor['zhangfu'] < 1.099]

        # dfMonitor = ['300153', '002835', '002695', '000025', '002302', '002822', '002591', '002510', '603767', '002282', '300112']

        dfPrintAll = pd.DataFrame()
        for i in range(0, len(dfMonitor)):
            code = dfMonitor.iloc[i]['code']
            name = dfMonitor.iloc[i]['name']

            # code = dfMonitor[i]

            s = pd.Series(index=['code', 'name', 'chubanCount', 'beizaLv', 'gaokaiLv', 'baobenLv', 'shoupanLv'])
            s[['code']] = s[['code']].astype(str)
            dfPrint = dfZhangtingHistory[dfZhangtingHistory['code'] == code]
            if len(dfPrint):
                s['code'] = code
                s['name'] = dfPrint.iloc[0]['name']
                s['chubanCount'] = dfPrint.iloc[0]['chubanCount']
                s['beizaLv'] = dfPrint.iloc[0]['beizaLv']
                s['gaokaiLv'] = dfPrint.iloc[0]['gaokaiLv']
                s['baobenLv'] = dfPrint.iloc[0]['baobenLv']
                s['shoupanLv'] = dfPrint.iloc[0]['shoupanLv']

                # print dfPrint[['code', 'name', 'chubanCount', 'beizaLv', 'gaokaiLv']]
            else:
                s['code'] = code
                s['name'] = name
                # print "no zhangting history: ", dfMonitor.iloc[i]['name']
            dfPrintAll = dfPrintAll.append(s, ignore_index=True)

        if len(dfPrintAll):
            print dfPrintAll[['code', 'name', 'chubanCount', 'beizaLv', 'gaokaiLv', 'baobenLv', 'shoupanLv']]


###################Zhangting Yizi, BeiZa, ZhengChang#######################

        dffshoufa = dff[dff['chuban']>1.4]
        print "shoufa: ", len(dffshoufa)

        dff = dff[dff['chuban']>1.099]
        print "before chuban.................: ", len(dff)
        dffchuban = dff[dff['chuban']<1.4]
        print "after chuban..................: ", len(dffchuban)


        #print dffchuban[['code', 'name', 'zf', 'a1_v']]
        print "jinri zhangting chuban: ", len(dffchuban)
        #print dffchuban['name']
        dffchuban.to_sql('rtChuBan', engine, index=False, if_exists='append')

        dffyizizhangting = dffchuban[dffchuban['low'] == dffchuban['high']]
        dffzhengchang = dffchuban[dffchuban['low'] != dffchuban['high']]
       # print dffzhengchang['name']
        #print dffyizikaipan[['code', 'name', 'zf']]

        dffyizizhangting = dffyizizhangting.append(dffshoufa)
        print "yizi zhangting......", len(dffyizizhangting)
        dffyizizhangting.to_sql('rtYiZi', engine, index=False, if_exists='append')

        dffzhangting = dffzhengchang[dffzhengchang['a1_p']==0]
        print "zhengchang zhangting liebiao......", len(dffzhangting)
        dffzhangting.to_sql('rtZhengChang', engine, index=False, if_exists='append')

        dffbeiza = dffzhengchang[dffzhengchang['a1_p'] > 0 ]
        print "zhangting beiza liebiao......", len(dffbeiza)
        dffbeiza.to_sql('rtBeiZa', engine, index=False, if_exists='append')

    else:
        continue






