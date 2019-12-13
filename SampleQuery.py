from pymongo import MongoClient


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['Sample']
record_generator = collection.find({'class': {'$ne': None}, 'audio_features': {'$ne': None}})
