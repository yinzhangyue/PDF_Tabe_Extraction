import pymongo

myclient = pymongo.MongoClient("mongodb://root:123456abc@10.23.58.215:27017/")
mydb = myclient["test"]
mydb.list_collection_names()