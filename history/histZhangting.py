from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import pymysql
import time
import datetime
import matplotlib.pyplot as plt

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')

print "reading stock codes from stockBasics..."
sql = "SELECT distinct code, name FROM `stockBasics`"
dfCode = pd.read_sql(sql, conn)

print "reading trading history from stockData2017..."
sql = "SELECT code, name, close, high, low, open, date FROM `stockData2017` order by date asc"
dfTrans = pd.read_sql(sql, conn)

#print (df)
print "start calculating..."
dfResult = pd.DataFrame()
for n in range(0, len(dfCode)):
    code = dfCode.iloc[n]['code']
    name = dfCode.iloc[n]['name']
    df = dfTrans[dfTrans['code'] == code]

    print n, code, name

    sLine = pd.Series(index=['date', 'code', 'name', 'zhangting', 'beiza', 'ciriOpen', 'ciriHigh', 'ciriClose'])

    for i in range(1, len(df)-1):
        if len(df) < 3:
            continue

        yestClose = df.iloc[i-1]['close']
        todayHigh = df.iloc[i]['high']
        todayLow = df.iloc[i]['low']
        todayClose = df.iloc[i]['close']
        tmrOpen = df.iloc[i+1]['open']
        tmrHigh = df.iloc[i+1]['high']
        tmrClose = df.iloc[i+1]['close']

        if (todayHigh / yestClose > 1.099 and todayLow != todayHigh):
            sLine['date'] = str(df.iloc[i]['date'])
            sLine['code'] = code
            sLine['name'] = name
            if todayHigh == todayClose:
                sLine['zhangting'] = 1
                sLine['beiza'] = 0
            else:
                sLine['zhangting'] = 0
                sLine['beiza'] = 1
            sLine['open'] = round ((tmrOpen / todayHigh - 1)*100, 2)
            sLine['high'] = round ((tmrHigh / todayHigh - 1)*100, 2)
            sLine['close'] = round ((tmrClose / todayHigh - 1)*100, 2)

            dfResult = dfResult.append(sLine, ignore_index=True)

print "writing to table - zhangtingHistory", len(dfResult)
engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')
dfResult.to_sql('histZhangting', engine, index=False, if_exists='append')
