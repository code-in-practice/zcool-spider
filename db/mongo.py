__author__ = 'smile'

from pymongo import MongoClient
import datetime

db_url = '127.0.0.1'
db_port = 27017
client = MongoClient(db_url, db_port)

db = client['zcool']
collection = db['user']

user = {"author": "Mike"}
print(user)
user_id = collection.insert_one(user).inserted_id
print(user_id)