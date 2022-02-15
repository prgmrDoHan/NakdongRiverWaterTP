from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

data=[]

conn = psycopg2.connect(host='ec2-44-193-188-118.compute-1.amazonaws.com', dbname='d59jrssgvr247h',user='qjqcjkjvhracnj',password='34ee13682cbe2cb0d4443247bd6e3dff51e15b3948e9997b5ae8abeb76aae644',port=5432)
cur = conn.cursor()

cur.execute('SELECT * FROM nakdong')
rows = cur.fetchall()
for row in rows:
    data.append(list(row))
conn.close()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/nakdong')
def nakdong():
    resjson={}
    resjson['waterTP']=data
    return jsonify(resjson)

@app.route('/nakdong/<riverNo>')
def nakdongOnlyOne(riverNo):
    resjson={}
    resjson['no']=riverNo
    resjson['waterTP']=data[int(riverNo)]
    return jsonify(resjson)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)