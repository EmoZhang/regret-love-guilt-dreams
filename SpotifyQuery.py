import time
import base64
from bson import json_util as json
import requests


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
        self.id = ''
        self.query = ''

    # Search a song
    def search(self, performer='', song=''):
        params = dict((
            ('q', 'artist:{} track:{}'.format(performer, song)),
            ('type', 'track'),
            ('market', 'US'),
            ('limit', '1'),
        ))
        self.query = params['q']
        while True:
            search_result = requests.get('https://api.spotify.com/v1/search', headers=self.headers, params=params)
            rate = check_rate_limiting(search_result)
            if rate is None:
                self.id = search_result.json()['tracks']['items'][0]['uri'].split(':')[2]
                break
            elif rate == 1:
                pass
            else:
                with open('search_error.txt', mode='a', encoding='utf8') as f:
                    f.write(self.query)
                    f.write('\n')
                    f.write(json.dumps(rate))
                    f.write('\n')
                return 1

    # Get Audio Features for a Track
    def get_audio_features(self):
        while True:
            track_features = requests.get('https://api.spotify.com/v1/audio-features/{}'.format(self.id),
                                          headers=self.headers)
            rate = check_rate_limiting(track_features)
            if rate is None:
                return track_features.json()
            elif rate == 1:
                pass
            else:
                with open('af_error.txt', mode='a', encoding='utf8') as f:
                    f.write(self.query)
                    f.write('\n')
                    f.write(json.dumps(rate))
                    f.write('\n')
                break

            # {'acousticness': 2.86e-05,
            #  'analysis_url': 'https://api.spotify.com/v1/audio-analysis/5ghIJDpPoe3CfHMGu71E6T',
            #  'danceability': 0.516,
            #  'duration_ms': 301920,
            #  'energy': 0.906,
            #  'id': '5ghIJDpPoe3CfHMGu71E6T',
            #  'instrumentalness': 0.000101,
            #  'key': 1,
            #  'liveness': 0.105,
            #  'loudness': -4.525,
            #  'mode': 1,
            #  'speechiness': 0.0658,
            #  'tempo': 116.775,
            #  'time_signature': 4,
            #  'track_href': 'https://api.spotify.com/v1/tracks/5ghIJDpPoe3CfHMGu71E6T',
            #  'type': 'audio_features',
            #  'uri': 'spotify:track:5ghIJDpPoe3CfHMGu71E6T',
            #  'valence': 0.728}


with open('client.txt', mode='r', encoding='utf8') as c:
    client_id, client_secret = c.read().split('\n')
s = AudioFeatures(client_id, client_secret)
record_list = [1]
for i in record_list:

    search_status = s.search(performer='Lana Del Rey', song='Norman Fucking Rockwell')
    if search_status is None:
        audio_features = s.get_audio_features()
        if audio_features is not None:
            pass  # wait for further supplements
