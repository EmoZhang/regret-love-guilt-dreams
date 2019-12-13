import time
import base64
from bson import json_util as json
import requests
from pymongo import MongoClient


def check_rate_limiting(r):
    if r.status_code == 200:
        pass
    elif r.status_code == 429:
        sleep_time = r.headers['Retry-After']
        print('Rate Limiting reached. Sleep for {}'.format(sleep_time))
        time.sleep(sleep_time)
        return 1
    elif r.status_code == 304:
        print('304 Not Modified')
        return r.json()
    else:
        print(r.status_code)
        print(r.json())
        return r.json()


class AudioFeatures:
    def __init__(self, client_id, client_secret):
        # Authorization
        self.client_id = client_id
        self.client_secret = client_secret
        client_base64 = base64.b64encode('{}:{}'.format(client_id, client_secret).encode('utf-8')).decode('utf-8')
        Authorization = 'Basic ' + client_base64
        headers_auth = {
            'Authorization': Authorization,
        }
        data = {
            'grant_type': 'client_credentials'
        }
        while True:
            response = requests.post('https://accounts.spotify.com/api/token', headers=headers_auth, data=data)
            rate = check_rate_limiting(response)
            if rate is None:
                self.access_token = response.json()['access_token']
                self.token_type = response.json()['token_type']
                self.headers = {
                    'Authorization': 'Bearer ' + self.access_token,
                }
                break
            elif rate == 1:
                pass
            else:
                raise RuntimeError('Authorization failed')
        self.query = ''

    # Search a song
    def search(self, performer, song):
        params = dict((
            ('q', 'artist:{} track:{}'.format(performer, song)),
            ('type', 'track'),
            ('market', 'US'),
            ('limit', '1'),
        ))
        self.query = params['q']

        def make_query(performer, song, round_flag):
            song_ = song.split(' (')[0].replace('F*ck', 'Fuck').replace('N****z', 'Niggaz').replace('S**t', 'Shit')
            performer_ = performer.split(' Featuring ')[0].split(' & ')[0].split(',')[0].split(' x ')[0].split(
                ' X ')[0].split(' / ')[0].split(' Co-Starring ')[0].split(' With ')[0].split(' Duet With ')[
                0].split(' vs ')[0].replace("'n'", " 'n' ").split(' (')[0].split(' Vs. ')[0]
            if round_flag == 1:
                query = '{} {}'.format(performer, song)
            elif round_flag == 2:
                query = 'artist:{} track:{}'.format(performer_, song_)
            else:
                query = '{} {}'.format(performer_, song_)
            return query

        round_flag = 0
        while True:
            search_result = requests.get('https://api.spotify.com/v1/search', headers=self.headers, params=params)
            rate = check_rate_limiting(search_result)
            if round_flag in [0, 1, 2]:
                if rate is None:
                    if search_result.json()['tracks']['total'] == 0:
                        params['q'] = make_query(performer=performer, song=song, round_flag=round_flag)
                        round_flag += 1
                    else:
                        track_id = search_result.json()['tracks']['items'][0]['uri'].split(':')[2]
                        song_name = search_result.json()['tracks']['items'][0]['name']
                        performer_name = ', '.join(
                            [item['name'] for item in search_result.json()['tracks']['items'][0]['artists']])
                        return track_id, song_name, performer_name
                elif rate == 1:
                    pass
                else:
                    self.error(genre='search', info=rate)
                    break
            else:
                if rate is None:
                    if search_result.json()['tracks']['total'] == 0:
                        self.error(genre='search', info=rate)
                        break
                    else:
                        track_id = search_result.json()['tracks']['items'][0]['uri'].split(':')[2]
                        song_name = search_result.json()['tracks']['items'][0]['name']
                        performer_name = ', '.join(
                            [item['name'] for item in search_result.json()['tracks']['items'][0]['artists']])
                        return track_id, song_name, performer_name
                elif rate == 1:
                    pass
                else:
                    self.error(genre='search', info=rate)
                    break

    # Get Audio Features for a Track
    def get_audio_features(self, track_id):
        while True:
            track_features = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(track_id),
                                          headers=self.headers)
            rate = check_rate_limiting(track_features)
            if rate is None:
                return track_features.json()
            elif rate == 1:
                pass
            else:
                self.error(genre='features', info=rate)
                break

    # Get Meta Info for a Track
    def get_a_track(self, track_id):
        while True:
            track_meta = requests.get('https://api.spotify.com/v1/tracks/{}'.format(track_id),
                                      headers=self.headers)
            rate = check_rate_limiting(track_meta)
            if rate is None:
                if track_meta is None:
                    self.error(genre='track', info=rate)
                    break
                else:
                    song_name = track_meta.json()['name']
                    performer_name = ', '.join(
                        [item['name'] for item in track_meta.json()['artists']])
                    return song_name, performer_name
            elif rate == 1:
                pass
            else:
                self.error(genre='track', info=rate)
                break

    def error(self, genre, info):
        with open('error_{}.txt'.format(genre), mode='a', encoding='utf8') as f:
            f.write(self.query)
            f.write('\n')
            f.write(json.dumps(info))
            f.write('\n')


def main():
    with open('client.txt', mode='r', encoding='utf8') as c:
        client_id, client_secret = c.read().split('\n')
    s = AudioFeatures(client_id, client_secret)
    record_list = [1]
    client = MongoClient(host='localhost', port=27017)
    db = client['Billboard']
    collection = db['Sample']

    records = collection.find({'audio_features': None, 'class': {'$exists': True}})
    for idx, record in enumerate(records):
        Performer = record['artists']
        Song = record['name']
        search_result = s.search(performer=Performer, song=Song)
        if search_result:
            track_id, song_name, performer_name = search_result
            if track_id:
                audio_features = s.get_audio_features(track_id=track_id)
                if audio_features:
                    collection.update_one({'name': Song, 'artists': Performer}, {
                        '$set': {'name_spotify': song_name, 'artists_spotify': performer_name,
                                 'audio_features': audio_features}})
                    print(idx + 1)
                    # print(audio_features)


if __name__ == '__main__':
    main()
