import json
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='lovetr', db='falcon', charset='utf8')
c = conn.cursor()


@app.route('/')
def hello():
    c.execute('select shangzhang, xiadie, pingpan from mon order by date, time desc limit 1')
    v = c.fetchone();
    conn.commit();
    ones = [v[0], v[1], v[2]];
    print ones
    return render_template('mon.html', data=json.dumps(ones))


@app.route('/new', methods=['GET'])
def getnew():
    c.execute('select shangzhang, xiadie, pingpan from mon order by date, time desc limit 1')
    v = c.fetchone()
    conn.commit();
    top = [v[0], v[1], v[2]]
    print top
    return json.dumps(top)


app.run(host='0.0.0.0', port=8888, debug=True)
