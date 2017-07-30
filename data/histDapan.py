import pandas as pd
import pymysql
from sqlalchemy import create_engine

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')

print "reading history from table histdata2017"
sql = "SELECT code, name, close, high, low, open, volume, date, p_change  FROM `histdata2017` where date>'2017-01-01' order by date asc "
dfAll = pd.read_sql(sql, conn)

print "reading date from table histdata2017"
sqlDate = "SELECT distinct date FROM `histdata2017` where date>'2017-01-01' order by date asc "
dfDate = pd.read_sql(sqlDate, conn)

print "start calculating..."
n = 0
dfResult = pd.DataFrame()
for i in range(0, len(dfDate)):
    date = dfDate.iloc[i]['date']
    df = dfAll[dfAll['date'] == date]
    sLine = pd.Series(
        index=['date', 'num', 'vol', 'avgzf', 'zhang', 'ping', 'die', 'zhangting', 'dieting',
               'fxy5', 'f5f2', 'f2f0', 'z0z2', 'z2z5', 'zdy5'])

    sLine['date'] = str(date)
    sLine['num'] = len(df)
    sLine['vol'] = round(df['volume'].sum() / 100000000.0, 2)
    sLine['avgzf'] = round(df['p_change'].sum() / len(df), 2)
    sLine['zhang'] = len(df[df['p_change']>0])
    sLine['ping'] = len(df[df['p_change']==0])
    sLine['die'] = len(df[df['p_change']<0])
    sLine['zhangting'] = len(df[df['p_change']>9.95])
    sLine['dieting'] = len(df[df['p_change']<-9.95])

    fxy9 = len(df[df['p_change']<-9])
    fxy8 = len(df[df['p_change']<-8])
    fxy7 = len(df[df['p_change']<-7])
    fxy6 = len(df[df['p_change']<-6])
    fxy5 = len(df[df['p_change']<-5])
    fxy4 = len(df[df['p_change']<-4])
    fxy3 = len(df[df['p_change']<-3])
    fxy2 = len(df[df['p_change']<-2])
    fxy1 = len(df[df['p_change']<-1])
    fxy0 = len(df[df['p_change']<-0])
    fz00 = len(df[df['p_change']==0])
    zdy0 = len(df[df['p_change']>0])
    zdy1 = len(df[df['p_change']>1])
    zdy2 = len(df[df['p_change']>2])
    zdy3 = len(df[df['p_change']>3])
    zdy4 = len(df[df['p_change']>4])
    zdy5 = len(df[df['p_change']>5])
    zdy6 = len(df[df['p_change']>6])
    zdy7 = len(df[df['p_change']>7])
    zdy8 = len(df[df['p_change']>8])
    zdy9 = len(df[df['p_change']>9])

    sLine['fxy5'] = fxy5
    sLine['f5f2'] = fxy2 - fxy5
    sLine['f2f0'] = fxy0 - fxy2
    sLine['z0z2'] = zdy0 - zdy2
    sLine['z2z5'] = zdy2 - zdy5
    sLine['zdy5'] = zdy5

    dfResult = dfResult.append(sLine, ignore_index=True)

print "writing to table - histDapan"
engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')
dfResult.to_sql('histDapan', engine, index=False, if_exists='append')

#    print fxy5,fxy2,fxy0,zdy0,zdy2,zdy5
