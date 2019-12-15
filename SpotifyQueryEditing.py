from bson.objectid import ObjectId
from pymongo import MongoClient
import requests
import pandas as pd
import SpotifyQuery

with open('client_1.txt', mode='r', encoding='utf8') as c:
    client_id, client_secret = c.read().split('\n')
s = SpotifyQuery.AudioFeatures(client_id, client_secret)

client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['ten_year']

# object_ids_str = """"""
#
# object_ids = object_ids_str.split('\n')
#
# URIs_str = """"""
#
# URIs = [i.replace('spotify:track:', '') for i in URIs_str.split('\n')]

notes = pd.read_csv('cleaning.csv')
query_df = notes[notes['note'] == '1'][['_id', 'URI']]
object_ids = list(query_df['_id'])
URIs = [i.replace('spotify:track:', '') for i in list(query_df['URI'])]

for idx, track_id in enumerate(URIs):
    track_meta = s.get_a_track(track_id=track_id)
    if track_meta:
        song_name, performer_name = track_meta
        print(performer_name, ' - ', song_name)
        audio_features = s.get_audio_features(track_id=track_id)
        datum = collection.find_one({'_id': ObjectId(object_ids[idx])})
        if audio_features:
            collection.update_one({'_id': ObjectId(object_ids[idx])}, {
                '$set': {'name_spotify': song_name, 'artists_spotify': performer_name,
                         'audio_features': audio_features}})
            print(idx + 1)
            print(audio_features)
