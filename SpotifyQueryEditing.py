from bson.objectid import ObjectId
from pymongo import MongoClient
import requests
import SpotifyQuery

with open('client.txt', mode='r', encoding='utf8') as c:
    client_id, client_secret = c.read().split('\n')
s = SpotifyQuery.AudioFeatures(client_id, client_secret)

client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['Sample']
object_ids_str = """5def6aa254d79fcf0de3ec92
5def6aa254d79fcf0de3ed22
5def6aa254d79fcf0de3ed91
5def6aa254d79fcf0de3eda3
5def6aa254d79fcf0de3ee3f
5def6aa254d79fcf0de3ee4c"""
object_ids = object_ids_str.split('\n')
URIs_str = """spotify:track:48td6xvpokdYwvbl3JIiXP
spotify:track:0a4HnQAiD08Yg8z30yfPhI
spotify:track:2Yia0Gh4n61fPAjrNE5i2t
spotify:track:6zGrmt2Ico8vRx8oDemgl6
spotify:track:6fmeXejj4CNkAQ78yao7oE
spotify:track:3VCWhe7AtBrkhour9t6dq6"""
URIs = [i.replace('spotify:track:', '') for i in URIs_str.split('\n')]

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
