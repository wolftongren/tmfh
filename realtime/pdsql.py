import pandas as pd
import numpy as np
import pymysql
import time
import datetime
import tushare as ts

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')


d = datetime.datetime.now().date()
sql = "select l.code, l.name, round(l.zf, 2), r.industry, x.cbTime from rtChuBan as l left join stockBasics as r on l.code=r.code left join rtChubanTime as x on x.code = l.code where x.date = '%s' and a1_p != 0 order by l.zf" % d
print sql
dfChubanTime = pd.read_sql(sql, conn)
print (dfChubanTime)
