from pymongo import MongoClient


client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection1 = db['10yWeekly']
collection2 = db['10yYearly']
ten = collection2.find()
count = 0
failure = []
temp = []
for i in ten:
    results_cursor = collection1.find({'Song': i['Song'], 'Performer': i['Performer']})
    results = [item for item in results_cursor]
    if len(results) == 1:
        count += 1
    elif len(results) == 0:
        failure.append(i)
    else:
        temp.append(i)

