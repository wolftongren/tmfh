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

sql = "select * from `histZhangtingStock1317`"
dfZhangtingHistory1317 = pd.read_sql(sql, conn)

sql = "select * from `histZhangtingStock2017`"
dfZhangtingHistory2017 = pd.read_sql(sql, conn)

d = datetime.datetime.now().date()
sql = "select * from `rtChubanTime` where date = '%s'" % d
dfChubanTime = pd.read_sql(sql, conn)

engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')

t925 = datetime.time(hour=9, minute=25, second=0)
t1130 = datetime.time(hour=11, minute=30, second=10)
t1300 = datetime.time(hour=13, minute=0, second=0)
t1500 = datetime.time(hour=15, minute=0, second=10)

t1455 = datetime.time(hour=14, minute=55, second=0)
t1459 = datetime.time(hour=14, minute=59, second=0)

#dfChubanTime = pd.DataFrame(columns=['date', 'code', 'name', 'cbTime', 'isBeiza'])


while True:

    print "sleeping 5s.."
    time.sleep(5)

    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()

    if t > t1500:
        print "stock is over, exit..."
        break

    if (t > t925 and t < t1130) or (t > t1300 and t < t1500):

        print "fetching data...", datetime.datetime.now()
        dfResult = pd.DataFrame()
        for i in range(0, len(dfstocks)/500+1):
            df = ts.get_realtime_quotes(dfstocks.iloc[i*500:(i+1)*500,0])
            if df is None:
                pass
            else:
                dfResult = dfResult.append(df)

        dff = dfResult.copy()

        dff = dff[dff['volume']>'0']


        dff['zhangfu'] = 0.0
        dff['chuban'] = 0.0
        dff['zf']=0.0
        dff['rtime']= datetime.datetime.now().strftime("%H:%M:%S")



        dff[['price']] = dff[['price']].astype(float)
        dff[['pre_close']] = dff[['pre_close']].astype(float)
        dff[['open']] = dff[['open']].astype(float)
        dff[['high']] = dff[['high']].astype(float)
        dff[['low']] = dff[['low']].astype(float)
        dff[['zf']] = dff[['zf']].astype(float)
        dff[['a1_p']] = dff[['a1_p']].astype(float)

        dff['zhangfu'] =  dff['price'] / dff['pre_close']
        dff['chuban'] = dff['high'] / dff['pre_close']
        dff['zf'] = (dff['price'] / dff['pre_close'] - 1) * 100


################### average zhangfu for all, 000, 300, 600 #############

        dff000 = dff[dff['code']< '300000']
        dfftmp = dff[dff['code'] > '300000']
        dff300 = dfftmp[dfftmp['code'] < '600000']
        dff600 = dff[dff['code'] >= '600000' ]

        avgzf = round(dff['zf'].sum() / len(dff), 2)
        avg000zf = round(dff000['zf'].sum() / len(dff000), 2)
        avg300zf = round(dff300['zf'].sum() / len(dff300), 2)
        avg600zf = round(dff600['zf'].sum() / len(dff600), 2)

        if not conn:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab',
                                   charset='utf8')
        sql = "insert into rtAvgZhangfu(date, time, avgzf, avg000zf, avg300zf, avg600zf ) values (%s, %s, %s, %s, %s, %s)"
        c = conn.cursor()
        tt = datetime.datetime.now().time().strftime('%H:%M')
        c.execute(sql, (d, tt, avgzf, avg000zf, avg300zf, avg600zf))
        conn.commit()
        c.close()


        
        ####################zhang die fu 1%######################
        
        fxy9 = len(dff[dff['zf'] < -9])
        fxy8 = len(dff[dff['zf'] < -8])
        fxy7 = len(dff[dff['zf'] < -7])
        fxy6 = len(dff[dff['zf'] < -6])
        fxy5 = len(dff[dff['zf'] < -5])
        fxy4 = len(dff[dff['zf'] < -4])
        fxy3 = len(dff[dff['zf'] < -3])
        fxy2 = len(dff[dff['zf'] < -2])
        fxy1 = len(dff[dff['zf'] < -1])
        fxy0 = len(dff[dff['zf'] < -0])
        fz00 = len(dff[dff['zf'] == 0])
        zdy0 = len(dff[dff['zf'] > 0])
        zdy1 = len(dff[dff['zf'] > 1])
        zdy2 = len(dff[dff['zf'] > 2])
        zdy3 = len(dff[dff['zf'] > 3])
        zdy4 = len(dff[dff['zf'] > 4])
        zdy5 = len(dff[dff['zf'] > 5])
        zdy6 = len(dff[dff['zf'] > 6])
        zdy7 = len(dff[dff['zf'] > 7])
        zdy8 = len(dff[dff['zf'] > 8])
        zdy9 = len(dff[dff['zf'] > 9])

        if not conn:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab',
                                   charset='utf8')
        sql = "insert into rtZhangDieFu(date, time, fxy9,fxy8,fxy7,fxy6,fxy5,fxy4,fxy3,fxy2,fxy1,fxy0,fz00,zdy0,zdy1,zdy2,zdy3,zdy4,zdy5,zdy6,zdy7,zdy8,zdy9) values (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
        c = conn.cursor()
        c.execute(sql, (d, t, fxy9,fxy8,fxy7,fxy6,fxy5,fxy4,fxy3,fxy2,fxy1,fxy0,fz00,zdy0,zdy1,zdy2,zdy3,zdy4,zdy5,zdy6,zdy7,zdy8,zdy9))
        conn.commit()
        c.close()
        
##############chuban, yizi, zhangting, beiza############

        dfChuban = dff[dff['chuban']>1.099]
        dfYizi = dfChuban[dfChuban['high']==dfChuban['low']]
        dfNotYizi = dfChuban[dfChuban['high']!=dfChuban['low']]
        dfZhangting = dfNotYizi[dfNotYizi['a1_p']==0]
        dfBeiza = dfChuban[dfChuban['a1_p'] !=0]

        chuban = len(dfChuban)
        yizi = len(dfYizi)
        zhangting = len(dfZhangting)
        beiza = len(dfBeiza)


        if t > t1455 and t < t1459:
            pass
        else:
            sql = "insert into rtZhangtingShu(date, time, chuban, yizi, zhangting, beiza ) values (%s, %s, %s, %s, %s, %s)"
            c = conn.cursor()
            tt = datetime.datetime.now().time().strftime('%H:%M')
            c.execute(sql, (d, tt,  chuban, yizi, zhangting, beiza))
            conn.commit()
            c.close()

        '''

##########################Zhang Die Ping##############################
        shangzhang = len(dff[dff['zhangfu'] > 1])
        xiadie = len(dff[dff['zhangfu'] < 1])
        pingpan = len(dff[dff['zhangfu'] == 1])
        if not conn:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')
        sql = "insert into rtZhangDiePing(date, time, shangzhang, xiadie, pingpan) values (%s, %s, %s, %s, %s)"
        c = conn.cursor()
        c.execute(sql, (d, t, shangzhang, xiadie, pingpan))
        conn.commit()
        c.close()
'''

##########################Daban Tishi##############################
        dfMonitor = dff[dff['zhangfu'] > 1.080]
        dfMonitor = dfMonitor[dfMonitor['zhangfu'] < 1.099]

        dfPrintAll = pd.DataFrame()
        for i in range(0, len(dfMonitor)):
            code = dfMonitor.iloc[i]['code']
            name = dfMonitor.iloc[i]['name']
            zf = dfMonitor.iloc[i]['zf']
            high = (dfMonitor.iloc[i]['high'] / dfMonitor.iloc[i]['pre_close'] - 1) * 100

            s = pd.Series(index=['code', 'name', 'zf', 'high', 'chubanCount3', 'beizaLv3', 'gaokaiLv3', 'baobenLv3', 'shoupanLv3', 'chubanCount', 'beizaLv', 'gaokaiLv', 'baobenLv', 'shoupanLv'])
            s[['code']] = s[['code']].astype(str)

            s['code'] = code
            s['name'] = name
            s['zf'] = round(zf, 2)
            s['high'] = round(high, 2)
            #data from 2013-2017
            dfPrint1317 = dfZhangtingHistory1317[dfZhangtingHistory1317['code'] == code]
            if len(dfPrint1317):
                s['chubanCount3'] = dfPrint1317.iloc[0]['chubanCount']
                s['beizaLv3'] = dfPrint1317.iloc[0]['beizaLv']
                s['gaokaiLv3'] = dfPrint1317.iloc[0]['gaokaiLv']
                s['baobenLv3'] = dfPrint1317.iloc[0]['baobenLv']
                s['shoupanLv3'] = dfPrint1317.iloc[0]['shoupanLv']

            #data from 2017-01-01 -- 2017-07-31
            dfPrint2017 = dfZhangtingHistory2017[dfZhangtingHistory2017['code'] == code]
            if len(dfPrint2017):
                s['chubanCount'] = dfPrint2017.iloc[0]['chubanCount']
                s['beizaLv'] = dfPrint2017.iloc[0]['beizaLv']
                s['gaokaiLv'] = dfPrint2017.iloc[0]['gaokaiLv']
                s['baobenLv'] = dfPrint2017.iloc[0]['baobenLv']
                s['shoupanLv'] = dfPrint2017.iloc[0]['shoupanLv']


            dfPrintAll = dfPrintAll.append(s, ignore_index=True)

        if len(dfPrintAll):
            dfPrintAll['date'] = datetime.datetime.now().date()
            dfPrintAll['rtime'] = datetime.datetime.now().strftime("%H:%M:%S")
            dfPrintAll.to_sql('rtDabanTishi', engine, index=False, if_exists='replace')


###################Zhangting Chuban --- Yizi, BeiZa, ZhengChang#######################

        dffchuban = dff[dff['chuban']>1.099]
        dffchuban.to_sql('rtChuBan', engine, index=False, if_exists='replace')

################### chubanTime, isBeiza ##########################

        dfMonitor = dff[dff['chuban'] > 1.099]
        dfBeiza = dfMonitor[dfMonitor['zhangfu'] < 1.099]

        for i in range(0, len(dfMonitor)):
            code = dfMonitor.iloc[i]['code']
            name = dfMonitor.iloc[i]['name']
            #zf = dfMonitor.iloc[i]['zf']
            d = dfMonitor.iloc[i]['date']
            t = dfMonitor.iloc[i]['time']
            #high = dfMonitor.iloc[i]['high']
            #low = dfMonitor.iloc[i]['low']
            #chuban = dfMonitor.iloc[i]['chuban']
            #zhangfu = dfMonitor.iloc[i]['zhangfu']
            #a1_p = dfMonitor.iloc[i]['a1_p']

            dfff = dfChubanTime[dfChubanTime['code'] == code]
            if len(dfff):  # already in the chuban list
                pass
            else:  # first time chuban
                s = pd.Series(index=['date', 'code', 'name', 'cbTime', 'isBeiza'])
                s[['code']] = s[['code']].astype(str)

                s['date'] = d
                s['code'] = code
                s['name'] = name
                s['cbTime'] = t
                s['isBeiza'] = 0
                dfChubanTime = dfChubanTime.append(s, ignore_index=True)

                if not conn:
                    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab',
                                           charset='utf8')
                sql = "insert into rtChubanTime(date, code, name, cbTime, isBeiza) values (%s, %s, %s, %s, %s)"
                c = conn.cursor()
                c.execute(sql, (d, code, name, t, 0))
                conn.commit()
                c.close()

#        print "chuban: "
#        print dfChubanTime
#        dfChubanTime.to_sql('rtChubanTime', engine, index=False, if_exists='replace')

        # update how many stocks BeiZa
        if not conn:
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')
        c = conn.cursor()
        for i in range(0, len(dfBeiza)):
            code = dfBeiza.iloc[i]['code']
            sql = "update rtChubanTime set isBeiza = 1 where code = %s"
            c.execute(sql, code)
        conn.commit()
        c.close()








