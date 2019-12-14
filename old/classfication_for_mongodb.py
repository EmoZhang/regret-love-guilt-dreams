from pymongo import MongoClient


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['Sample']
f = collection.find()

love_tags = ['Sex', 'Seduction', 'Romantic Evening', 'In Love', 'New Love', 'Wedding', 'Romance']
breakup_tags = ['D-I-V-O-R-C-E', 'Breakup']


def update_class(song, performer, class_):
    collection.update_one({'name': song, 'artists': performer}, {'$set': {'class': class_}})


for record in f:
    for tag in record['tags']:
        if tag in love_tags and tag in breakup_tags:
            if record['song'] == 'Find Your Love':
                update_class(song=record['name'], performer=record['artists'], class_='Love')
            else:
                update_class(song=record['name'], performer=record['artists'], class_='Breakup')
        else:
            if tag in love_tags:
                update_class(song=record['name'], performer=record['artists'], class_='Love')
            if tag in breakup_tags:
                update_class(song=record['name'], performer=record['artists'], class_='Breakup')
