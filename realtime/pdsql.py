import pandas as pd
import numpy as np
import pymysql
import time
import datetime
import tushare as ts

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')

while True:
    time.sleep(10)

    if not conn:
        print "connetion is broken"

    else:
        print datetime.datetime.now(), "connection is OK"

'''

  
d = datetime.datetime.now().date()
#d = "'2017-08-04'"
sql = "select * from rtChubanTime where date = '%s'" % d
print sql
dfChubanTime = pd.read_sql(sql, conn)
print (dfChubanTime)
'''