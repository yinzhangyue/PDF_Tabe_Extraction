import pymongo
from pymongo import MongoClient

host = '192.168.0.14'  # 记得修改成MongoDB的主节点
username = 'root'
password = '123456abc'
port = '27017'
db = 'pdfTableDetection'
mongo_url = 'mongodb://{0}:{1}@{2}:{3}/'.format(username, password, host, port)
myclient = pymongo.MongoClient(mongo_url)
mydb = myclient[db]
# collist = mydb.list_collection_names()
# print(collist)
filename = "0"
info = {0: ['1a'], 1: ['2a'], 2: ['3a'], 3: []}
pages = max(info.keys())
info = str(info)
# info = eval(info)
location = "/root/pdfTableDetection/Files/0"
mydict = {
    "filename": filename,
    "info": info,
    "pages": pages,
    "location": location
}
print(mydict)
mycol = mydb["pdfInfo"]
mycol.insert_one(mydict)
for x in mycol.find():
    print(x)
