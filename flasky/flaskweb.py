# encoding = utf-8

import json
import pymysql
import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='stocklab', charset='utf8')


@app.route('/')
def root():
    return render_template('dapan.html')


@app.route('/dapan')
def dapan():
    return render_template('dapan.html')


@app.route('/zhangting')
def zhangting():
    return render_template('zhangting.html')


@app.route('/daban')
def daban():
    return render_template('daban.html')


@app.route('/mon')
def mon():
    return render_template('mon.html')


@app.route('/zhangdiefujson', methods=['GET'])
def zhangdiepfu():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute(
        'select fxy9,fxy8,fxy7,fxy6,fxy5,fxy4,fxy3,fxy2,fxy1,fxy0,fz00,zdy0,zdy1,zdy2,zdy3,zdy4,zdy5,zdy6,zdy7,zdy8,zdy9 from rtZhangDieFu where date = %s order by time desc limit 1',
        d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        top = [v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15],
               v[16], v[17], v[18], v[19], v[20]]
    else:
        top = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    return json.dumps(top)


@app.route('/avgzhangfujson', methods=['GET'])
def avgzhangfu():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute(
        'select distinct time, avgzf, avg000zf, avg300zf, avg600zf from rtAvgZhangfu where date = %s order by time', d)
    v = c.fetchall()
    conn.commit()
    c.close()

    if (v != None):
        avgzf = []
        avg000zf = []
        avg300zf = []
        avg600zf = []
        for row in v:
            avgzf.append(row[1])
            avg000zf.append(row[2])
            avg300zf.append(row[3])
            avg600zf.append(row[4])
        return json.dumps([avgzf, avg000zf, avg300zf, avg600zf])
    else:
        return json.dumps([[0], [0], [0], [0]])


@app.route('/avgzhangfutablejson', methods=['GET'])
def avgzhangfutable():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute(
        'select distinct time, avgzf, avg000zf, avg300zf, avg600zf from rtAvgZhangfu where date = %s order by time desc limit 1',
        d)
    v = c.fetchone()
    conn.commit()
    c.close()

    if (v != None):
        res = [{'id': '1', 'name': 'all', 'zhangfu': v[1]}, {'id': '2', 'name': '000', 'zhangfu': v[2]},{'id': '3', 'name': '300', 'zhangfu': v[3]},{'id': '4', 'name': '600', 'zhangfu': v[4]}]
        print json.dumps(res)
        return json.dumps(res)
    else:
        return json.dumps([[0], [0], [0], [0]])


@app.route('/zhangtingsplinejson')
def monsplinejson():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select distinct time, yizi from rtZhangtingShu where date = %s order by time', d)
    v1 = c.fetchall()
    c.execute('select distinct time, zhangting from rtZhangtingShu where date = %s order by time', d)
    v2 = c.fetchall()
    c.execute('select distinct time, beiza from rtZhangtingShu where date = %s order by time', d)
    v3 = c.fetchall()
    conn.commit()
    c.close()

    if (v1 != None):
        return json.dumps([v1, v2, v3])
    else:
        return json.dumps([[0], [0], [0], [0]])


@app.route('/monjson')
def monjson():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select shangzhang, xiadie, pingpan from rtZhangDiePing where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        return json.dumps([['zhang', v[0]], ['die', v[1]], ['ping', v[2]]])
    else:
        return json.dumps([['zhang', 8], ['die', 1], ['ping', 14]])


@app.route('/dabantishijson', methods=['GET'])
def dabantishijson():
    c = conn.cursor()
    c.execute(
        "select code, name, round(zf,2), chubancount3, beizaLv3, gaokaiLv3, baobenLv3, shoupanLv3, chubanCount, beizaLv, gaokaiLv, baobenLv, shoupanLv, high from rtDabanTishi")
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i = 1
        for row in v:
            result = {}
            result['id'] = i
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

            i = i + 1
            jsonData.append(result)

        return json.dumps(jsonData)


@app.route('/chubanjson', methods=['GET'])
def zhangtingjson():
    c = conn.cursor()
    c.execute("select code, name, zf, a1_v from rtChuBan where 1")
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        for row in v:
            result = {}
            result['code'] = row[0]
            result['name'] = row[1]
            result['pchange'] = row[2]
            result['a1_b'] = row[3]
            jsonData.append(result)

        return json.dumps(jsonData)


@app.route('/yizijson', methods=['GET'])
def yizijson():
    #    sql = "select y.code, y.name, b.timeToMarket from stockBasics as b right join rtYiZi as y on y.code = b.code order by b.timeToMarket desc"
    sql = "select l.code, l.name, r.timeTomarket from rtChuBan as l left join stockBasics as r on l.code=r.code where low = high or zhangfu > 1.4 order by r.timeToMarket desc"
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
            result['id'] = i
            result['code'] = row[0]
            result['name'] = row[1]
            result['timeToMarket'] = row[2]

            i = i + 1
            jsonData.append(result)
        return json.dumps(jsonData)


@app.route('/beizajson', methods=['GET'])
def beizajson():
    c = conn.cursor()
    d = datetime.datetime.now().date()
    sql = "select l.code, l.name, round(l.zf, 2), r.industry, x.cbTime from rtChuBan as l left join stockBasics as r on l.code=r.code left join rtChubanTime as x on x.code = l.code where x.date = '%s' and a1_p != 0 order by x.cbTime" % d
    c.execute(sql)
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i = 1
        for row in v:
            result = {}
            result['id'] = i
            result['code'] = row[0]
            result['name'] = row[1]
            result['zf'] = row[2]
            result['industry'] = row[3]
            result['cbTime'] = row[4]

            i = i + 1
            jsonData.append(result)
        print jsonData
        return json.dumps(jsonData)


@app.route('/zhengchangjson', methods=['GET'])
def zhengchangjson():
    c = conn.cursor()
    d = datetime.datetime.now().date()
    sql = "select l.code, l.name, r.industry, x.cbTime, x.isBeiza from rtChuBan as l left join stockBasics as r on l.code=r.code left join rtChubanTime as x on x.code = l.code where x.date = '%s' and a1_p = 0 and low != high and zhangfu < 1.4 order by x.cbTime" % d
    c.execute(sql)
    v = c.fetchall()
    conn.commit()
    c.close()
    if (v != None):
        jsonData = []
        i = 1
        for row in v:
            result = {}
            result['id'] = i
            result['code'] = row[0]
            result['name'] = row[1]
            result['industry'] = row[2]
            result['cbTime'] = row[3]
            result['isBeiza'] = row[4]
            i = i + 1
            jsonData.append(result)
        return json.dumps(jsonData)


app.run(host='0.0.0.0', port=8888, debug=True)
