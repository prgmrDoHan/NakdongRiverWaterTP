from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/nakdong')
def nakdong():
    adata=[]

    conn = psycopg2.connect(host=os.environ['host'], dbname=os.environ['database'],user=os.environ['user'],password=os.environ['dbPassword'],port=5432)
    cur = conn.cursor()

    cur.execute('SELECT * FROM nakdong')
    rows = cur.fetchall()
    for row in rows:
        adata.append(list(row))
    conn.close()
    resjson={}
    resjson['waterTP']=adata
    return jsonify(resjson)

@app.route('/nakdong/<riverNo>')
def nakdongOnlyOne(riverNo):
    bdata=[]

    conn = psycopg2.connect(host=os.environ['host'], dbname=os.environ['database'],user=os.environ['user'],password=os.environ['dbPassword'],port=5432)
    cur = conn.cursor()

    cur.execute('SELECT * FROM nakdong')
    rows = cur.fetchall()
    for row in rows:
        bdata.append(list(row))
    conn.close()
    resjson={}
    resjson['no']=riverNo
    resjson['waterTP']=bdata[int(riverNo)]
    return jsonify(resjson)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
