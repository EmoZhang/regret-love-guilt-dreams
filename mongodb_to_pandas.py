import pandas as pd
from pandas.io.json import json_normalize
from pymongo import MongoClient

client = MongoClient()
db = client['Billboard']
collection = db['ten_year']
query = {
    'name_spotify': {'$not': {'$eq': 'NNN/AAA'}}
}
df = json_normalize(list(collection.find(query)))
df.columns = [col.replace('audio_features.', '') for col in df.columns]
df.drop(['analysis_url', 'track_href', 'type', '_id', 'artists_spotify', 'name_spotify'], axis=1)
df = df[['id', 'class', 'artists', 'name', 'acousticness', 'danceability',
         'duration_ms', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'mode',
         'key', 'time_signature']]
# df = df[['_id', 'class', 'artists', 'artists_spotify', 'name', 'name_spotify']]
df.to_csv('Billboard_ten_years.tsv', sep='\t', header=True, index=False)
df.to_csv('Billboard_ten_years.csv', sep=',', header=True, index=False)
df.to_excel('Billboard_ten_years.xlsx', header=True, index=False)
