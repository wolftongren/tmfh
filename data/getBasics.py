#coding=utf-8

from sqlalchemy import create_engine
import tushare as ts


df = ts.get_stock_basics()
print len(df)
engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')
df.to_sql('basics', engine, if_exists='append')