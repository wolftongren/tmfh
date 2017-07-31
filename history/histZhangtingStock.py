from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import pymysql
import time
import datetime

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')

print "reading distinct code from zhangtingHistory..."
sql = "SELECT distinct code, name FROM `histZhangting`"
dfStocks = pd.read_sql(sql, conn)

print "reading zhangting history from zhangtingHistory..."
sql = "SELECT * FROM `histZhangting`"
dfData = pd.read_sql(sql, conn)

print "start calculating..."
dfResult = pd.DataFrame()
for i in range(0, len(dfStocks)):

    sLine = pd.Series(index=['code', 'name', 'chubanCount', 'beizaLv', 'gaokaiLv', 'baobenLv', 'shoupanLv'])

    code = dfStocks.iloc[i]['code']
    df = dfData[dfData['code'] == code]

    zhangtingCount = len(df[df['zhangting']==1.0])
    beizaCount = len(df[df['beiza']==1.0])
    ciriOpenCount = len(df[df['ciriOpen']>0])
    ciriHighCount = len(df[df['ciriHigh']>0])
    ciriCloseCount = len(df[df['ciriClose']>0])
    chubanCount = zhangtingCount + beizaCount
    beizaLv = round (beizaCount*1.0 / chubanCount * 100, 2)
    gaokaiLv = round (ciriOpenCount*1.0 / chubanCount * 100, 2)
    baobenLv = round (ciriHighCount*1.0 / chubanCount * 100, 2)
    shoupanLv = round (ciriCloseCount*1.0 / chubanCount * 100, 2)

    sLine[['code']] = sLine[['code']].astype(str)
    sLine['code'] = str(code)
    sLine['name'] = dfStocks.iloc[i]['name']
    sLine['chubanCount'] = chubanCount
    sLine['beizaLv'] = beizaLv
    sLine['gaokaiLv'] = gaokaiLv
    sLine['baobenLv'] = baobenLv
    sLine['shoupanLv'] = shoupanLv


    dfResult = dfResult.append(sLine, ignore_index=True)


print "writing to table - histZhangtingStock", len(dfResult)
engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')
dfResult.to_sql('histZhangtingStock', engine, index=False, if_exists='append')