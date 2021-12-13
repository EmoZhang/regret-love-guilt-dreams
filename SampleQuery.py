from pymongo import MongoClient


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['ten_year']
record_generator = collection.find({'audio_features': {'$ne': None}})
