import asyncio
import time
from lxml import etree
import aiohttp
from pymongo import MongoClient
from bson import json_util as json


async def job(session, URL):
    async with session.get(URL) as response:
        # response = await session.get(URL).text()  # 等待并切换
        return await response.text()


all_results = []


async def main(loop):
    global all_results
    async with aiohttp.ClientSession() as session:  # 官网推荐建立 Session 的形式
        tasks = [loop.create_task(job(session, url.format(i))) for i in range(2009, 2019)]
        finished, unfinished = await asyncio.wait(tasks)
        all_results = [r.result() for r in finished]  # 获取所有结果


def parse(response):
    html = etree.HTML(response)
    container = '//*[@id="main"]/div[5]/div'
    ranks = html.xpath(container + '//div[@class="ye-chart-item__rank"]/text()')
    titles = html.xpath(container + '//div[@class="ye-chart-item__title"]/text()')
    artists = html.xpath(container + '//div[@class="ye-chart-item__artist"]')
    ranks = [int(r.strip().strip('\n')) for r in ranks]
    titles = [r.strip().strip('\n').replace(r"\'", "'") for r in titles]
    artists = [r.xpath('string(.)').strip().strip('\n') for r in artists]
    year = int(html.xpath('//*[@id="main"]/div[5]/div/div[1]/div[1]/div[1]/div/span/button/span[1]/text()')[0])
    if year == 2016:
        titles.insert(86, 'All the Way Up')
        ranks.insert(86, 87)
        artists.insert(86, 'Fat Joe, Remy Ma and Jay-Z featuring French Montana and Infared')
    if year == 2011:
        titles.insert(6, 'Fuck You')
        ranks.insert(6, 7)
        artists.insert(6, 'Cee Lo Green')
    songs = []
    for i in range(100):
        j = {
            'Song': titles[i],
            'Performer': artists[i],
            'Rank': ranks[i],
            'Year': year
        }
        songs.append(j)
    return songs


url = 'https://www.billboard.com/charts/year-end/{}/hot-100-songs'
t1 = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
t2 = time.time()
print('atiohttp', t2 - t1)

t3 = time.time()
client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['10yYearly']
for idx, result in enumerate(all_results):
    song_list = parse(result)
    __ = collection.insert_many([song for song in json.loads(json.dumps(song_list))])
print('parse & save', t3 - t2)
