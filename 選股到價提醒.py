from __future__ import print_function
import time
from linebot import (LineBotApi, WebhookHandler, exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import schedule
import pymongo
from pymongo import MongoClient
import urllib.parse
import datetime
import requests
from bs4 import BeautifulSoup

collection = '資料庫名稱'
line_bot_api = LineBotApi('LINE_CHANNEL_ACCESS_TOKEN')
yourid='你的User ID'

Authdb='資料庫名稱'
def constructor():
    client = pymongo.MongoClient("mongodb+srv://<你的hostname>:<password>@cluster0.tbiz4.mongodb.net/myfirstdb?retryWrites=true&w=majority")
    db = client[Authdb]
    return db

def show_user_stock_function():
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"data": 'care_stock'}))
    return cel

def job():
    data = show_user_stock_function()
    for i in data:
        stock=i['stock']
        bs=i['bs']
        price=i['price']

        url = 'https://tw.stock.yahoo.com/q/q?s=' + stock
        list_req = requests.get(url)
        soup = BeautifulSoup(list_req.content, "html.parser")
        getstock = soup.find('b').text
        if float(getstock):
            if bs == '<':
                if float(getstock) < price:
                    get=stock + '的價格:' + getstock
                    line_bot_api.push_message(yourid,TextSendMessage(text=get))

            else:
                if float(getstock) > price:
                    get=stock + '的價格:' + getstock
                    line_bot_api.push_message(yourid,TextSendMessage(text=get))
        else:
            line_bot_api.push_message(yourid,TextSendMessage(text='這個有問題'))

#second_5_j = schedule.every(10).seconds.do(job)
#while True:
    #schedule.run_pending()
    #time.sleep(1)
job()
