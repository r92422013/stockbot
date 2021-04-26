from pymongo import MongoClient
import pymongo
import urllib.parse
import datetime

Authdb='資料庫名稱'
def constructor():
    client = pymongo.MongoClient("mongodb+srv://<你的hostname>:<password>@cluster0.tbiz4.mongodb.net/myfirstdb?retryWrites=true&w=majority")
    db = client[Authdb]
    return db

constructor()

def write_user_stock_function(stock, bs, price):
    db=constructor()
    collect = db['mystock']
    collect.insert({"stock": stock,
                    "data": 'care_stock',
                    "bs": bs,
                    "price": float(price),
                    "date_info": datetime.datetime.utcnow()
                    })

def delete_user_stock_function(stock):
    db=constructor()
    collect = db['mystock']
    collect.remove({"stock": stock})
    
def show_user_stock_function():
    db=constructor()
    collect = db['mystock']
    cel=list(collect.find({"data": 'care_stock'}))
    return cel
