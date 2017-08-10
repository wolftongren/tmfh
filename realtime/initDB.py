# coding=utf-8

import pymysql
import datetime

d = datetime.datetime.now().date()
t = datetime.datetime.now().time()
print d, t
print "running initDB.py"
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')

print "deleting rtDabanTishi"
sql1 = "delete from rtDabanTishi"
print "deleting rtChuBan"
sql2 = "delete from rtChuBan"

c = conn.cursor()
c.execute(sql1)
c.execute(sql2)
conn.commit()
c.close()

print "finished running initDB.py"
d = datetime.datetime.now().date()
t = datetime.datetime.now().time()
print d, t
print ""
