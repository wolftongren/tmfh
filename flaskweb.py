import json
import pymysql
import datetime
from flask import Flask, request, render_template

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='falcon', charset='utf8')
c = conn.cursor()


@app.route('/')
def hello():
    d = datetime.datetime.now().date()
    c.execute('select shangzhang, xiadie, pingpan from mon where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    if (v != None):
        ones = [v[0], v[1], v[2]]
    else:
        ones = [0,0,0]
    print ones
    return render_template('mon.html', data=json.dumps(ones))


@app.route('/new', methods=['GET'])
def getnew():
    d = datetime.datetime.now().date()
    c.execute('select shangzhang, xiadie, pingpan from mon where date = %s order by time desc limit 1', d)
    v = c.fetchone()
    conn.commit()
    if (v!=None):
        top = [v[0], v[1], v[2]]
    else:
        top = [0,0,0]
    print top
    return json.dumps(top)



app.run(host='0.0.0.0', port=8888, debug=True)
