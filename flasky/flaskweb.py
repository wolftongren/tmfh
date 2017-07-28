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


@app.route('/chubanjson', methods=['GET'])
def zhangtingjson():
    # data = [{"code":"603525", "name":"xxxxxx", "pchange":"8.77", "a1_b":"222"}, {"code":"603525", "name":"xxxxxx", "pchange":"8.77", "a1_b":"222"},{"code":"603525", "name":"xxxxxx", "pchange":"8.77", "a1_b":"222"}]
    # return json.dumps(data)

    d = datetime.datetime.now().date()
    t = datetime.datetime.now().strftime("%H:%M:%S")
    c = conn.cursor()
    c.execute("select code, name, zf, a1_v from rtChuBan where date = %s order by time desc limit 50", d)
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

        print "jsonData: ", jsonData
        return json.dumps(jsonData)


@app.route('/yizijson', methods=['GET'])
def yizijson():
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().strftime("%H:%M:%S")
    c = conn.cursor()
    c.execute("select rtime, count(*) as num from rtYiZi where date = %s group by rtime order by rtime desc", d)
    v = c.fetchone()
    num = v[1]

    sql = "select y.code, y.name, b.timeToMarket from rtYiZi as y join stockBasics as b on y.code = b.code where date = %s order by rtime desc limit %s"
    c.execute(sql, (d,num))

    #c.execute("select code, name from yizi where date = %s order by rtime desc limit %s", (d, num) )
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

        print "jsonData: ", jsonData
        return json.dumps(jsonData)


@app.route('/beizajson', methods=['GET'])
def beizajson():
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().strftime("%H:%M:%S")
    c = conn.cursor()
    c.execute("select rtime, count(*) as num from rtBeiZa where date = %s group by rtime order by rtime desc", d)
    v = c.fetchone()
    num = v[1]

    c.execute("select code, name, round(zf,2) from rtBeiZa where date = %s order by rtime desc limit %s", (d, num) )
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

            i=i+1
            jsonData.append(result)

        print "jsonData: ", jsonData
        return json.dumps(jsonData)


@app.route('/zhengchangjson', methods=['GET'])
def zhengchangjson():
    d = datetime.datetime.now().date()
    t = datetime.datetime.now().strftime("%H:%M:%S")
    c = conn.cursor()
    c.execute("select rtime, count(*) as num from rtZhengChang where date = %s group by rtime order by rtime desc", d)
    v = c.fetchone()
    num = v[1]

    c.execute("select code, name from rtZhengChang where date = %s order by rtime desc limit %s", (d, num) )
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

            i=i+1
            jsonData.append(result)

        print "jsonData: ", jsonData
        return json.dumps(jsonData)




app.run(host='0.0.0.0', port=8888, debug=True)
