from bson.objectid import ObjectId
from pymongo import MongoClient
import discogs_client
import SpotifyQuery


class DC(discogs_client.Client):
    def __init__(self, user_agent, user_token="bMvFJjAcVYOPbqSLRGDdktJGrFDJbNIfBScWFphr"):
        super(DC, self).__init__(user_agent, user_token=user_token)

    def get_album_info(self, album: str) -> dict:
        """
        Get information of the main release of the master release of the given album.
        :param album: recommended syntax: <artist> - <album>
        :return: a dictionary containing 6 key info of the album.
        """
        results = self.search(album, type='master')
        try:
            master_release = results[0]
            main_release = master_release.main_release
            title_ = main_release.title
            try:
                styles = ', '.join([style for style in master_release.data['styles']])
            except KeyError:
                try:
                    styles = ', '.join([style for style in main_release.data['styles']])
                except KeyError:
                    styles = ''
            try:
                album_info = {
                    # 'title': master_release.title,
                    # 'artists': ' / '.join([dict_['name'] for dict_ in master_release.data['artists']]),
                    'genres': ', '.join([genre for genre in master_release.genres]),
                    'styles': styles,
                }
            except KeyError:
                album_info = None
        except IndexError:
            results = self.search(album, type='release')
            try:
                release = results[0]
                genres = release.genres
                try:
                    styles = ', '.join([style for style in release.data['styles']])
                except KeyError:
                    styles = ''
                try:
                    album_info = {
                        # 'title': release.title,
                        # 'artists': ' / '.join([item.name for item in release.artists]),
                        'genres': ', '.join(genres),
                        'styles': styles,
                    }
                except KeyError:
                    album_info = None
            except IndexError:
                album_info = None

        return album_info


with open('client_1.txt', mode='r', encoding='utf8') as c:
    client_id, client_secret = c.read().split('\n')
s = SpotifyQuery.AudioFeatures(client_id, client_secret)

client = MongoClient(host='localhost', port=27017)
db = client['Billboard']
collection = db['ten_year']
records = collection.find(
    {
        '$and': [
            {'genres': []},
            {'audio_features': {'$ne': 'NNN/AAA'}},
            {'audio_features': {'$ne': None}}
        ]
    },
    {'_id': 1, 'audio_features.id': 1, 'artists_spotify': 1, 'album': 1}
)

records = list(records)
# q = len(records) // 50
# r = len(records) % 50
# if r == 0:
#     track_threads = len(records) // 50
# else:
#     track_threads = len(records) // 50 + 1
#
artists = [record['artists_spotify'].split(', ')[0] for record in records]
_ids = [record['_id'] for record in records]
# ids = [record['audio_features']['id'] for record in records]
album_names = [record['album'] for record in records]

# for i in range(track_threads):
#     while True:
#         try:
#             if i != track_threads - 1:
#                 tracks_meta = s.get_several_tracks(track_ids=ids[50 * i: 50 * (i + 1)])
#             else:
#                 tracks_meta = s.get_several_tracks(track_ids=ids[50 * i:])
#             if tracks_meta['tracks']:
#                 names_part = [item['album']['name'].split(' (')[0] for item in tracks_meta['tracks']]
#                 album_names.extend(names_part)
#                 print(i + 1, '/', track_threads, 'track threads')
#                 break
#             else:
#                 raise RuntimeError('Failed to get tracks')
#         except:
#             pass
# print('Get tracks done')
# if len(records) != len(album_names):
#     raise ValueError('len(records) != len(album_names)')
#
# for i in range(len(records)):
#     collection.update_one({'_id': _ids[i]}, {'$set': {'album': album_names[i]}})

genres_list = []
style_list = []


d = DC('BNA update/1.0')
for i in range(len(album_names)):
    while True:
        try:
            album_info = d.get_album_info(artists[i] + ' - ' + album_names[i])
            if album_info:
                genres_list.append(album_info['genres'])
                style_list.append(album_info['styles'])
            else:
                genres_list.append('')
                style_list.append('')
            collection.update_one({'_id': _ids[i]},
                                  {'$set': {'genres': genres_list[i], 'styles': style_list[i]}})
            print(i + 1, '/', len(album_names), 'albums')
            break
        except Exception as e:
            print(artists[i] + ' - ' + album_names[i] + ':', e)
        pass

print('Get albums done')
if len(records) != len(genres_list) or len(records) != len(style_list):
    raise ValueError('len(records) != len(genres_list)')
