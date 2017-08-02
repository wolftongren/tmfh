# encoding = utf-8

import json
import pymysql
import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')


@app.route('/')
def hello():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select shangzhang, xiadie, pingpan from rtZhangDiePing where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        ones = [v[0], v[1], v[2]]
    else:
        ones = [0, 0, 0]
    return render_template('main.html', data=json.dumps(ones))


@app.route('/zhangdie', methods=['GET'])
def getnew():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select shangzhang, xiadie, pingpan from rtZhangDiePing where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        top = [v[0], v[1], v[2]]
    else:
        top = [0, 0, 0]
    return json.dumps(top)


@app.route('/mon')
def index():
    return render_template('mon.html', data=json.dumps([1, 1, 1]))


@app.route('/zhangting')
def zhangting():
    return render_template('zhangting.html')


@app.route('/dabantishijson', methods=['GET'])
def dabantishijson():

    c = conn.cursor()
    c.execute("select code, name, round(zf,2), chubancount3, beizaLv3, gaokaiLv3, baobenLv3, shoupanLv3, chubanCount, beizaLv, gaokaiLv, baobenLv, shoupanLv, high from rtDabanTishi")
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i=1
        for row in v:
            result = {}
            # print "row[0]: ", row[0]
            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['zf'] = row[2]
            result['high'] = row[13]
            result['chubanCount3'] = row[3]
            result['beizaLv3'] = row[4]
            result['gaokaiLv3'] = row[5]
            result['baobenLv3'] = row[6]
            result['shoupanLv3'] = row[7]
            result['chubanCount'] = row[8]
            result['beizaLv'] = row[9]
            result['gaokaiLv'] = row[10]
            result['baobenLv'] = row[11]
            result['shoupanLv'] = row[12]

            i=i+1
            jsonData.append(result)

#        print "dabantishijson: ", i, jsonData
        return json.dumps(jsonData)


@app.route('/chubanjson', methods=['GET'])
def zhangtingjson():
    # data = [{"code":"603525", "name":"xxxxxx", "pchange":"8.77", "a1_b":"222"}, {"code":"603525", "name":"xxxxxx", "pchange":"8.77", "a1_b":"222"},{"code":"603525", "name":"xxxxxx", "pchange":"8.77", "a1_b":"222"}]
    # return json.dumps(data)

    c = conn.cursor()
    c.execute("select code, name, zf, a1_v from rtChuBan where 1")
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        for row in v:
            result = {}
            # print "row[0]: ", row[0]

            result['code'] = row[0]
            result['name'] = row[1]
            result['pchange'] = row[2]
            result['a1_b'] = row[3]

            jsonData.append(result)

        return json.dumps(jsonData)


@app.route('/yizijson', methods=['GET'])
def yizijson():

    sql = "select y.code, y.name, b.timeToMarket from stockBasics as b right join rtYiZi as y on y.code = b.code order by b.timeToMarket desc"
#   sql = "select y.code, y.name from rtYiZi as y where 1"
    c = conn.cursor()
    c.execute(sql)

    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i = 1
        for row in v:
            result = {}
            # print "row[0]: ", row[0]
            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['timeToMarket'] = row[2]

            i=i+1
            jsonData.append(result)

 #       print "yizijson: ", i, jsonData
        return json.dumps(jsonData)


@app.route('/beizajson', methods=['GET'])
def beizajson():

    c = conn.cursor()
    sql = "select y.code, y.name, round(y.zf,2), s.industry from rtBeiZa as y left join stockBasics as s on y.code = s.code order by y.zf"
    c.execute(sql)
 #   c.execute("select code, name, round(zf,2) from rtBeiZa where 1")
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i=1
        for row in v:
            result = {}
            # print "row[0]: ", row[0]
            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['zf'] = row[2]
            result['industry'] = row[3]

            i=i+1
            jsonData.append(result)

        print "beizajson: ", i, jsonData
        return json.dumps(jsonData)


@app.route('/zhengchangjson', methods=['GET'])
def zhengchangjson():

    c = conn.cursor()
    c.execute("select l.code, l.name, r.industry from rtZhengChang as l left join stockBasics as r on l.code=r.code ")
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i=1
        for row in v:
            result = {}

            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['industry'] = row[2]


            i=i+1
            jsonData.append(result)

#        print "zhengchangjson: ", i, jsonData
        return json.dumps(jsonData)




app.run(host='0.0.0.0', port=8888, debug=True)
