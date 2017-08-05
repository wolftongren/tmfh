import pandas as pd
import numpy as np
import pymysql
import time

while True:

    print "sleeping 5s..."
    time.sleep(5)

    print "after sleep."
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')


    c = conn.cursor()
    for i in range(0, 1):
        code = '000525'
        sql = "update rtChubanTime set isBeiza = 1 where code = %s"
        c.execute(sql, code)
    conn.commit()
    c.close()

