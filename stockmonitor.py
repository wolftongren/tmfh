import tushare as ts
import pandas as pd
import pymysql
import time
import datetime

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stockdata', charset='utf8')
sql = "SELECT distinct code, name FROM `basics`"
dfstocks = pd.read_sql(sql, conn)
conn.close()

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='falcon', charset='utf8')
c = conn.cursor()


t930 = datetime.time(hour=9, minute=30, second=0)
t1130 = datetime.time(hour=11, minute=30, second=10)
t1300 = datetime.time(hour=13, minute=0, second=0)
t1500 = datetime.time(hour=15, minute=0, second=10)

while True:

    time.sleep(30)

    d = datetime.datetime.now().date()
    t = datetime.datetime.now().time()

    if (t < t930 and t < t1130) or (t > t1300 and t > t1500):
        print "fetching data...", datetime.datetime.now()
        dfResult = pd.DataFrame()
        for i in range(0, len(dfstocks) / 500 + 1):
            df = ts.get_realtime_quotes(dfstocks.iloc[i * 500:(i + 1) * 500, 0])
            if df is None:
                pass
            else:
                dfResult = dfResult.append(df)

        dfResult['zhangfu'] = 0.0

        dff = dfResult[dfResult['volume'] > '0']
        dff[['price']] = dff[['price']].astype(float)
        dff[['pre_close']] = dff[['pre_close']].astype(float)

        dff['zhangfu'] = dff['price'] / dff['pre_close']

        shangzhang = len(dff[dff['zhangfu'] > 1])
        xiadie = len(dff[dff['zhangfu'] < 1])
        pingpan = len(dff[dff['zhangfu'] == 1])

        sql = "insert into mon(date, time, shangzhang, xiadie, pingpan) values (%s, %s, %s, %s, %s)"
        c.execute(sql, (d, t, shangzhang, xiadie, pingpan))
        conn.commit()

    else:
        continue
