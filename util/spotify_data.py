import json
import os
import spotipy
import spotipy.util as spotipy_util

spotify_embed_url = 'https://open.spotify.com/embed/track/'
spotify_username = os.getenv('SPOTIPY_USERNAME')
spotify_token = spotipy_util.prompt_for_user_token(spotify_username)
spotify_client = spotipy.Spotify(auth=spotify_token)

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
data_dir = os.path.join(root_dir, 'data')
rasc_path = os.path.join(data_dir, 'rasc.json')

with open(rasc_path, 'r') as f:        
    rasc_json = json.load(f)

for season in rasc_json['seasons']:
    for episode in season['episodes']:
        for track in episode['tracks']:
            if track.get('no_music'):
                continue
            spotify_track = spotify_client.search('artist:' + track['artist']\
                            + ' track:' + track['title'], type='track')
            if len(spotify_track['tracks']['items']) == 0:
                print('No results from Spotify track search - artist: {}, track: {}'\
                    .format(track['artist'], track['title']))
                continue
            spotify_artist = spotify_client.artist(
                                spotify_track['tracks']['items'][0]['artists'][0]['id'])
            if len(spotify_artist['images']) == 0:
                artist_image = 'no_image_found'
            else:
                artist_image = spotify_artist['images'][-2]['url']
            track['artist_image'] = artist_image
            track['spotify_track_url'] = spotify_embed_url + spotify_track['tracks']['items'][0]['id']

with open(rasc_path, 'w') as json_file:
    json.dump(rasc_json, json_file, indent=2)