from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/nakdong')
def nakdong():
    adata=[]

    conn = psycopg2.connect(host='ec2-44-193-188-118.compute-1.amazonaws.com', dbname='d59jrssgvr247h',user='qjqcjkjvhracnj',password='34ee13682cbe2cb0d4443247bd6e3dff51e15b3948e9997b5ae8abeb76aae644',port=5432)
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

    conn = psycopg2.connect(host='ec2-44-193-188-118.compute-1.amazonaws.com', dbname='d59jrssgvr247h',user='qjqcjkjvhracnj',password='34ee13682cbe2cb0d4443247bd6e3dff51e15b3948e9997b5ae8abeb76aae644',port=5432)
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
