from pymongo import MongoClient
from bson import json_util as json


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection2 = db['10yYearly']
f = collection2.find()
results = [i for i in f]
result_dict = {}
for item in results:
    Song = item['Song']
    Performer = item['Performer']
    SongID = Performer + '+' + Song
    try:
        result_dict[SongID]['Billboard'].append({
            'Rank': item['Rank'],
            'Year': item['Year']
        })
    except KeyError:
        result_dict[SongID] = {
            'Song': Song,
            'Performer': Performer,
            'Billboard': [{
                'Rank': item['Rank'],
                'Year': item['Year']
            }]
        }
hot_list = [v for k, v in result_dict.items()]
collection2.drop()
result = collection2.insert_many([song for song in json.loads(json.dumps(hot_list))])
