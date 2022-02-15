import requests
import psycopg2
import time
from apscheduler.schedulers.background import BackgroundScheduler

def update():
    conn = psycopg2.connect(host='ec2-44-193-188-118.compute-1.amazonaws.com', dbname='d59jrssgvr247h',user='qjqcjkjvhracnj',password='34ee13682cbe2cb0d4443247bd6e3dff51e15b3948e9997b5ae8abeb76aae644',port=5432)
    cur = conn.cursor()

    URL= "http://koreawqi.go.kr/web/autoMeasure/list/itemList"
    data= {'ATTR_1':'R02'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = requests.post(URL, data=data, headers=headers)
    res.raise_for_status()

    itemData=res.json()['itemData']
    All = []
    date = time.strftime('%Y%m%d', time.localtime(time.time()))

    for i in range(0,len(itemData)):
        URL= "http://koreawqi.go.kr/web/autoMeasure/noConfirm/toastList"
        data= {
            'dFielNm':'%EB%AF%B8%ED%99%95%EC%A0%95+%EC%9E%90%EB%A3%8C+%EC%A1%B0%ED%9A%8C',
            'excelSnsNos':'',
            'pMENU_NO':'6',
            'page':'1',
            'ATTR_2':str(int(date)-1),
            'ATTR_3':str(int(date)-1),
            'querySn':'60',
            'queryTp':'autoMe',
            'station_code':itemData[i]['WQAMN_CODE'],
            'river':'R02',
            'pStartDay':'2022-02-15',
            'pEndDay':'2022-02-15',
            'pageSize':'10'
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        res = requests.post(URL, data=data, headers=headers)
        res.raise_for_status()
        data=res.json()['list'][0]
        All.append([i,data['WQAMN_NM'],data['IEM_WTRTP']])

    databaseInputData=[]
    for i in All:
        databaseInputData.append(tuple(i))

    print(databaseInputData)

    cur.execute('DELETE FROM nakdong')
    cur.executemany(
        'INSERT INTO public.nakdong (no,measuring,temperature) VALUES (%s, %s, %s)',
        databaseInputData
    )

    conn.commit()
    conn.close()

sched = BackgroundScheduler(timezone='Asia/Seoul')

@sched.scheduled_job('cron', hour=1)
def scheduled_job():
    update()

sched.start()