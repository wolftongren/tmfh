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


@app.route('/zhangdiefu', methods=['GET'])
def zhangdiepfu():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select fxy9,fxy8,fxy7,fxy6,fxy5,fxy4,fxy3,fxy2,fxy1,fxy0,fz00,zdy0,zdy1,zdy2,zdy3,zdy4,zdy5,zdy6,zdy7,zdy8,zdy9 from rtZhangDieFu where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        top = [v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13],v[14],v[15],v[16],v[17],v[18],v[19],v[20]]
    else:
        top = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    return json.dumps(top)



@app.route('/zhangdieping', methods=['GET'])
def zhangdieping():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select xiadie, pingpan, shangzhang from rtZhangDiePing where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        top = [v[0], v[1], v[2]]
    else:
        top = [0, 0, 0]
    top = [2018, 96, 889]
    return json.dumps(top)


@app.route('/zhangdiefive', methods=['GET'])
def zhangdiefive():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select shangzhang, xiadie, pingpan from rtZhangDiePing where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        top = [v[0], v[1], v[2]]
    else:
        top = [3, 20, 869, 1258, 69, 21];


    top = [3, 20, 869, 1258, 69, 21];
    return json.dumps(top)

@app.route('/zhangdieten', methods=['GET'])
def zhangdieten():
    d = datetime.datetime.now().date()
    c = conn.cursor()
    c.execute('select shangzhang, xiadie, pingpan from rtZhangDiePing where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    c.close()
    if (v != None):
        top = [v[0], v[1], v[2]]
    else:
        top = [7, 2, 9, 24, 12, 21, 222, 125, 332, 543, 645, 222, 342, 122, 87, 67, 23, 12, 5, 32];

    top = [7, 2, 9, 24, 12, 21, 222, 125, 332, 543, 645, 222, 342, 122, 87, 67, 23, 12, 5, 32];
    return json.dumps(top)


@app.route('/mon')
def mon():
    return render_template('mon.html')

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
        return json.dumps([['zhang', 1], ['die', 1], ['ping', 1]])


@app.route('/monsplinejson')
def monsplinejson():
    return json.dumps([6,7,5,4,3,4,5,6,6,7,8,9,38,26,18,22,9,5])



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
            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['timeToMarket'] = row[2]

            i=i+1
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
        i=1
        for row in v:
            result = {}
            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['zf'] = row[2]
            result['industry'] = row[3]
            result['cbTime'] = row[4]

            i=i+1
            jsonData.append(result)

        print "beizajson: ", i, jsonData
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
        i=1
        for row in v:
            result = {}
            result['id']=i
            result['code'] = row[0]
            result['name'] = row[1]
            result['industry'] = row[2]
            result['cbTime'] = row[3]
            result['isBeiza'] = row[4]
            i=i+1
            jsonData.append(result)
        return json.dumps(jsonData)




app.run(host='0.0.0.0', port=9999, debug=True)
