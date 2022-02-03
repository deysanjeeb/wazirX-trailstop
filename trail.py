from wazirx_sapi_client.rest import Client
from wazirx_sapi_client.websocket import WebsocketClient

import time
import  websocket,json, pprint
from websocket import create_connection
from time import sleep
import logging
import pandas as pd
import asyncio
import socket, threading
import json, sys, os, time, csv, requests


from flask import Flask,request
from flask import render_template
from flask import current_app as app
from os.path import exists

file_exists = exists("config.py")
if file_exists:
    import config
    api_key = config.API_KEY
    secret_key = config.SECRET_KEY
    client = Client(api_key=api_key, secret_key=secret_key)
    print(client.send("ping"))
    global wes
    wes = create_connection("wss://stream.wazirx.com/stream")
    print(wes)
    print("connection true")


# api_key = config.API_KEY
# secret_key = config.SECRET_KEY

app = Flask(__name__)
app.app_context().push()


def sellTrail(price):
    return(client.send('create_order',
              {"symbol": "ethinr", "side": "sell", "type": "stoplimit", "price": (price-price*0.003), "stopPrice":price,"quantity": quan, "recvWindow": 5000,
               "timestamp": int(time.time()*1000)}))

def updateTrail(tick,orderID,price,trail_tage,quan):
    try:
        print(client.send('cancel_order',
                {"symbol": tick, "orderId": orderID, "recvWindow": 5000, "timestamp": int(time.time()*1000)}))
    except:
        sleep(10)
        print(client.send('cancel_order',
                {"symbol": tick, "orderId": orderID, "recvWindow": 5000, "timestamp": int(time.time()*1000)}))

    sleep(5)
    try:
        return(client.send('create_order',
        {"symbol": tick, "side": "sell", "type": "stop_limit", "price": (price-price*trail_tage), "stopPrice":(price-price*(trail_tage-0.001)),"quantity": quan, "recvWindow": 5000,
               "timestamp": int(time.time()*1000)}))
    except:
        sleep(5)
        return(client.send('create_order',
        {"symbol": tick, "side": "sell", "type": "stop_limit", "price": (price-price*trail_tage), "stopPrice":(price-price*(trail_tage-0.001)),"quantity": quan, "recvWindow": 5000,
               "timestamp": int(time.time()*1000)}))

def gen_sign(query):
    t=int(time.time())
    echo = subprocess.Popen(['echo','-n',query], stdout=subprocess.PIPE, shell=False)
    hmac_key=subprocess.Popen(['openssl','dgst','-sha256','-hmac',API_SECRET],stdin=echo.stdout,stdout=subprocess.PIPE,shell=False)
    output = hmac_key.communicate()[0]
    output=str(output.strip())
    output=output.replace("b'(stdin)= ",'')
    output=output.replace("'" ,'')
    print(output)

def get_order(orderID):
    try:
        return(client.send('query_order',
              {"orderId": orderID, "recvWindow": 10000, "timestamp": int(time.time() * 1000)}))
    except:
        sleep(10)
        return(client.send('query_order',
              {"orderId": orderID, "recvWindow": 10000, "timestamp": int(time.time() * 1000)}))

async def send_heartbeat( *args):
    while True:
        print(wes.send(json.dumps({'event': 'ping'})))
        print("Beat sent")
        await asyncio.sleep(10*60)


@app.route("/", methods=["GET"])
def home():
    file_exists = exists("config.py")
    if file_exists:
        # api_key = config.API_KEY
        # secret_key = config.SECRET_KEY
        # global client
        # global wes
        # client = Client(api_key=api_key, secret_key=secret_key)
        # print(client.send("ping"))
        # wes = create_connection("wss://stream.wazirx.com/stream")
        # print(wes)
        open_ord=client.send('open_orders',
              {"recvWindow": 5000,
               "timestamp": int(time.time()*1000)})
        # print("Ticker: ")
        # tick=input()
        # print("Quantity: ")
        # quan=float(input())
        # print("Trail %: ")
        # trail_tage=float(input())
        # print("orderId: ")
        # orderId=int(input())
        # print("sellPrice: ")
        # sPrice=float(input())

        sleep(5)
        wes.send(json.dumps({
            "event": "subscribe",
            "streams": ["!ticker@arr"]
        }))
        print(file_exists)
        return render_template("dashboard.html",open_ord=open_ord,action="parameters")
    else:
        return render_template("login.html")

# @app.route("/dashboard", methods=["GET"])
# def dashboardShow():
#     return trail(tick,quan,trail_tage,orderId,sPrice,wes)

@app.route("/dashboard", methods=["POST"])
def dashboard():
    global tick
    global quan
    global trail_tage
    global orderId
    global sPrice
    tick=request.form['tick']
    quan=float(request.form['quan'])
    trail_tage=float(request.form['trail_tage'])
    orderId=request.form['orderId']
    sPrice=float(request.form['sPrice'])
    r=get_order(orderId)
    # render_template("dashboard.html",stat=r,action="display")
    trail(tick,quan,trail_tage,orderId,sPrice,wes)
    # render_template("dashboard.html",stat=r,action="display")

@app.route("/login", methods=["POST"])
def login():
    api_key=request.form['apiKey']
    secret_key=request.form['secretKey']
    save=request.form['save']
    if save=='True':
        file = open("config.py", "w")
        file.write("API-KEY = '"+api_key+"'\n")
        file.write("SECRET_KEY = '"+secret_key+"'\n")
        file.close()
    # global client
    # global wes
    client = Client(api_key=api_key, secret_key=secret_key)
    print(client.send("ping"))
    wes = create_connection("wss://stream.wazirx.com/stream")
    print(wes)
    return render_template("dashboard.html",open_ord=open_ord,action="parameters")




# _thread = threading.Thread(target=asyncio.run, args=(self.send_heartbeat(),))
# _thread.start()




def trail(tick,quan,trail_tage,orderId,sPrice,wes):
    # connections = dict()
    # connections["websocket"] = wes
    _thread = threading.Thread(target=asyncio.run, args=(send_heartbeat(),))
    _thread.start()
    result = wes.recv()
    res = json.loads(result)

    data={}
    recvd=False
    while not recvd:
        result = wes.recv()
        res = json.loads(result)
        stream=res['data']
        for dc in stream:
            if isinstance(dc,dict):
            # print(dc['s'])
            # for keys in dc:
            #   print(keys)
                if dc['s']==tick:
                    data=dc
                    recvd=True
    print("data",data['b'])

    col_heads=['Bought','MinSell','SoldP','Comp','BuyOrderID','BuyStatus','SellOrderID','SellStatus']
    ob = []
    prices=[]
    buy_order={}
    rows={}

    # print(data)
    bestSell=float(data['a'])
    bestBuy=float(data['b'])
    rows['serverTime']=data['E']
    rows['bestBuy']=bestBuy
    rows['bestSell']=bestSell
    df=pd.DataFrame()
    row=pd.DataFrame()
    row = row.append(rows, ignore_index=True, sort=False)
    row['serverTime']= pd.to_datetime(row['serverTime'], unit='ms')
    df = df.append(row, ignore_index=True, sort=False)
    print(row.loc[0])
    row_ls=row.values.tolist()
    # print(row_ls)
    prices.append(row_ls[0])
    print('prices',prices)


    while True:
        recvd=False
        while not recvd:
            try:
                result = wes.recv()
            except:
                sleep(30)
                wes = create_connection("wss://stream.wazirx.com/stream")

                print(wes)
                sleep(5)
                wes.send(json.dumps({
                    "event": "subscribe",
                    "streams": ["!ticker@arr"]
                }))
                # connections = dict()
                # connections["websocket"] = wes

            res = json.loads(result)
            # pprint.pprint(res)
            stream=res['data']
            for dc in stream:
                if isinstance(dc,dict):
                    if dc['s']==tick:
                        data=dc
                        recvd=True

        bestBuy=float(data['b'])
        bestSell=float(data['a'])
        times=data['E']
        rows={}
        rows['serverTime']=data['E']
        rows['bestBuy']=bestBuy
        rows['bestSell']=bestSell
        row=pd.DataFrame()
        row = row.append(rows, ignore_index=True, sort=False)
        row['serverTime']= pd.to_datetime(row['serverTime'], unit='ms')
        df = df.append(row, ignore_index=True, sort=False)
        print("Best sell price",bestSell)
        row_ls=row.values.tolist()

        prices.append(row_ls[0])
        try:
            r=get_order(orderId)
        except:
            sleep(10)
            r=get_order(orderId)
        status=r[1]
        # print(status)
        if status['status']=="done":
            print("complete")
            # render_template("dashboard.html",action="complete")
            break
        elif bestSell>int(sPrice):
            r=updateTrail(tick,orderId,bestSell,trail_tage,quan)
            stat=r[1]
            orderId=stat['id']
            sPrice=bestSell
            print(stat)
            # return render_template("dashboard.html",stat=stat,action="display")
            sleep(15)
        sleep(5)




app.app_context().push()
if __name__ == '__main__':
    app.run(host='localhost',port=8080, debug=True)