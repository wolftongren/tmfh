#coding=utf-8

import tushare as ts
import pandas as pd
import pymysql
from sqlalchemy import create_engine

dfstocks = ts.get_stock_basics()
dfstocks.reset_index(inplace = True)
print "total stock num: ", len(dfstocks)

dfResult = pd.DataFrame()

engine = create_engine('mysql+pymysql://root:lovetr@127.0.0.1/stocklab?charset=utf8')
for i in range(0, len(dfstocks)):
    print i, dfstocks['code'][i]
    # modify the api, start and end date here......
    df = ts.get_k_data(dfstocks['code'][i], autype=None, start='2017-06-10', end='2017-07-31')
    if df is None:
        pass
    else:
        df.reset_index(inplace = True)
        df['code']=dfstocks['code'][i]
        df['name']= dfstocks['name'][i]

        dfResult = dfResult.append(df, ignore_index=True)

#modify the database table name here
dfResult.to_sql('histKdataNone1317', engine,  index=False, if_exists='append')

