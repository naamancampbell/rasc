import json
import os
import spotipy
import spotipy.util as spotipy_util
import sys

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

playlist = []

for season in rasc_json['seasons']:
    for episode in season['episodes']:
        for track in episode['tracks']:
            if track.get('no_music'):
                continue
            spotify_track = spotify_client.search(
                                'artist:' + track['artist'] + ' track:' + \
                                track['title'], type='track', limit=5)
            if len(spotify_track['tracks']['items']) == 0:
                print('No results from Spotify search - artist: {}, track: {}'\
                    .format(track['artist'], track['title']))
                continue
            track_id = spotify_track['tracks']['items'][0]['id']
            if track_id not in playlist:
                playlist.append(track_id)
            spotify_artist = spotify_client.artist(
                                spotify_track['tracks']['items'][0]\
                                ['artists'][0]['id'])
            if len(spotify_artist['images']) == 0:
                artist_image = 'no_image_found'
            else:
                artist_image = spotify_artist['images'][-2]['url']
            track['artist_image'] = artist_image
            track['spotify_track_url'] = spotify_embed_url + \
                spotify_track['tracks']['items'][0]['id']

with open(rasc_path, 'w') as json_file:
    json.dump(rasc_json, json_file, indent=2)

if sys.argv[1] == '--create-playlist':
    playlist_name = sys.argv[2]
    response = spotify_client.user_playlist_create(
                user=spotify_username, name=playlist_name)
    playlist_id = response['id']
    response = spotify_client.user_playlist_add_tracks(
        user=spotify_username,
        playlist_id=playlist_id,
        tracks=playlist)    