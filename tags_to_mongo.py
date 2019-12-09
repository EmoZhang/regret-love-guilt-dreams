from pymongo import MongoClient
from bson import json_util as json


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection1 = db['10yWeekly']
collection2 = db['10yYearly']

record_list = []
with open('records.txt', mode='r', encoding='utf8') as f:
    records = f.readlines()
    for i in records:
        __, Performer, Song, tag_str = i.replace('\n', '').split('<>')
        tags = tag_str.split(',')
        record_list.append([Song, Performer, tags])

for record in record_list:
    Song, Performer, tags = record
    collection1.update_one({'Song': Song, 'Performer': Performer}, {'$set': {'tags': tags}}, upsert=False)

