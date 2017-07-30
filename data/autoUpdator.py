from sqlalchemy import create_engine
import tushare as ts
import pandas as pd
import pymysql
import datetime

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')
cur = conn.cursor()
engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')


print "updating basics..."
########## updating basics
sql = "SELECT distinct code, name FROM `basics`"
dfOld = pd.read_sql(sql, conn)
print "Old len:", len(dfOld)

df = ts.get_stock_basics()
df.reset_index(inplace = True)
print "New len:", len(df)

if len(df) > len(dfOld):
    print "deleting all data from the basics table"
    delsql = "DELETE FROM `basics`"
    cur.execute(delsql)
    conn.commit()
    print "writing new data into the basics table"
    df.to_sql('basics', engine, if_exists='append')


########## updating hist17
print "updating history2017..."
t = datetime.datetime.now()
todayDate = str(t.date())
print todayDate

dfResult = pd.DataFrame()
for i in range(0, len(df)):
    print i, df['code'][i]
    dfStock = ts.get_hist_data(df['code'][i], start=todayDate, end=todayDate)
    if dfStock is None:
        print "pass..."
        pass
    else:
        dfStock.reset_index(inplace = True)
        dfStock['code']=df['code'][i]
        dfStock['name']= df['name'][i]
        dfResult = dfResult.append(dfStock, ignore_index=True)

print "writing to history2017..."
dfResult.to_sql('history2017', engine,  index=False, if_exists='append')

cur.close()
conn.close()

