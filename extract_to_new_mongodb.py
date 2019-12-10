from pymongo import MongoClient


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection1 = db['10yWeekly']
collection2 = db['10yYearly']
f = collection1.find({'Performer': {'$regex': '^((?!Glee).)*$'}})
record_list = []
for i in f:
    Song, Performer = i['Song'], i['Performer']
    try:
        j = collection2.find({'Song': Song, 'Performer': Performer})
        result = [item for item in j]
        tags = i['tags']
        if len(result) == 0:
            record_list.append({
                'artists': Performer,
                'name': Song,
                'tags': tags,
                'type': 'Non-hit'
            })
        else:
            record_list.append({
                'artists': Performer,
                'name': Song,
                'tags': tags,
                'type': 'Hit'
            })
    except KeyError:
        pass
# love_tags = ['Sex', 'Seduction', 'Romantic Evening', 'In Love', 'New Love', 'Wedding', 'Romance']
# breakup_tags = ['D-I-V-O-R-C-E', 'Breakup']
#
#
# for record in record_list:
#     for tag in record['tags']:
#         if tag in love_tags:
#             record['class'] = 'love'
#         if tag in breakup_tags:
#             record['class_'] = 'breakup'
collection3 = db['Sample']
# collection3.insert_many(record_list)

