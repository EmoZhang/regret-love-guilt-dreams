# %%
import time
import pandas as pd

CSV_FILE_PATH = 'Hot Stuff.csv'
# %%
df = pd.read_csv(CSV_FILE_PATH)


def time_convert(format_time):
    ts = time.strptime(format_time, "%m/%d/%Y")
    timestamp = int(time.mktime(ts))
    return timestamp


week_stamp_list = []
week_bool_list = []
for i in range(len(df)):
    week_stamp = time_convert(df['WeekID'][i])
    week_stamp_list.append(week_stamp)
    if 1230768000 <= week_stamp < 1546300800:
        week_bool_list.append(True)
    else:
        week_bool_list.append(False)
#%%
last_ten_years = df.loc[week_bool_list, ]
df_copy = df.copy()
df = last_ten_years
#
#%%
import hashlib
hot_dict = {}
for i in range(len(df)):
    print(i)
    row = df.iloc[i]
    # SongID = base64.b64encode(row['SongID'].encode(encoding='utf8')).decode(encoding='utf8')
    SongID = hashlib.sha224(row['SongID'].encode(encoding='utf8')).hexdigest()
    billboard = {
        'WeekID': row['WeekID'],
        'Week Position': int(row['Week Position']),
        'Instance': int(row['Instance']),
        'Peak Position': int(row['Peak Position']),
        'Weeks on Chart': int(row['Weeks on Chart']),
    }
    try:
        billboard['Previous Week Position'] = int(row['Previous Week Position'])
    except ValueError:
        billboard['Previous Week Position'] = None
    try:
        hot_dict[SongID]['Billboard'].append(billboard)
        hot_dict[SongID]['Total Weeks'] = max(int(row['Weeks on Chart']), hot_dict[SongID]['Total Weeks'])
        hot_dict[SongID]['Final Peak Position'] = min(int(row['Peak Position']),
                                                             hot_dict[SongID]['Final Peak Position'])
    except KeyError:
        hot_dict[SongID] = {
            'Song': row['Song'],
            'Performer': row['Performer'],
            'Billboard': [billboard]
        }
        hot_dict[SongID]['Total Weeks'] = int(row['Weeks on Chart'])
        hot_dict[SongID]['Final Peak Position'] = int(row['Peak Position'])
#%%
from bson import json_util as json
hot_list = json.dumps([v for k, v in hot_dict.items()])
with open('Billboard 2009-2018 Weekly.json', mode='w', encoding='utf8') as f:
    f.write(hot_list)
#%%
from pymongo import MongoClient
client = MongoClient(host='localhost', port=27017)
dblist = client.list_database_names()
print(dblist)
#%%
db = client['Billboard']
collist = db.list_collection_names()
print(collist)
collection = db['10yWeekly']
#%%
# with open('Billboard.json', mode='r', encoding='utf8') as f:
#     j = f.read(hot_list)
# result = collection.insert_many([song for song in json.loads(hot_list)])
#%%

