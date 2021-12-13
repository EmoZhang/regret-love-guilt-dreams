from pymongo import MongoClient
import pandas


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection1 = db['10yWeekly']
collection2 = db['10yYearly']
f = collection1.find({'Performer': {'$regex': '^((?!Glee).)*$'}})
record_list = []
no_record_list = []
for i in f:
    Song, Performer = i['Song'], i['Performer']
    try:
        j = collection2.find({'Song': Song, 'Performer': Performer})
        result = [item for item in j]
        if len(result) == 0:
            tags = i['tags']
            no_record_list.append([Performer, Song, tags])
        else:
            tags = i['tags']
            record_list.append([Performer, Song, tags])
    except KeyError:
        pass


def flatten(rlist: list, y):
    rlist_a = []
    for j in rlist:
        for i in j[2]:
            rlist_a.append([j[0], j[1], i, y])
    return rlist_a


record_list_a = flatten(record_list, 'Hits')
no_record_list_a = flatten(no_record_list, 'Non-hits')
df = pandas.DataFrame((record_list_a + no_record_list_a), columns=['Performer', 'Song', 'Tag', 'Type'])
df.to_csv('song-tag-mapping.csv')
