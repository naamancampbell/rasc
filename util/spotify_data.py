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
rasc_path = os.path.join(root_dir, 'rasc.json')

with open(rasc_path, 'r') as f:        
    rasc_json = json.load(f)

rasc_md_path = os.path.join(root_dir, 'rasc.md')
os.remove(rasc_md_path)
rasc_md = open(rasc_md_path, 'a', encoding='utf-8')

for season in rasc_json['seasons']:
    season_title = list(season.keys())[0]
    print('# ' + season_title, file=rasc_md)
    for episode in season[season_title]:
        episode_title = list(episode.keys())[0]
        print('## ' + episode_title, file=rasc_md)
        for track in episode[episode_title]:
            scene_image = 'https://renandstimpymusic.files.wordpress.com/2016/12/stimpysbigday2.jpg?w=310&h=234'
            if track.get('no_music'):
                print('#### ' + track['no_music'], file=rasc_md)
                continue
            spotify_track = spotify_client.search('artist:' + track['artist']\
                            + ' track:' + track['title'], type='track')
            if len(spotify_track['tracks']['items']) == 0:
                print('No results from Spotify search - artist: {}, track: {}'\
                    .format(track['artist'], track['title']))
                continue
            spotify_artist = spotify_client.artist(
                                spotify_track['tracks']['items'][0]['artists'][0]['id'])           
            track_markdown = '|![' + track['scene'] + '](' + scene_image + ')'\
                             + '<br /> ' + track['time'] + ' - ' \
                             + track['scene'] + '|' \
                             + '![' + track['artist'] + '](' \
                             + spotify_artist['images'][-2]['url'] + ')|' \
                             + spotify_artist['name'] + ' <br /> ' \
                             + spotify_track['tracks']['items'][0]['name'] + ' <br /><br /> ' \
                             + '<iframe src="' + spotify_embed_url + spotify_track['tracks']['items'][0]['id'] + '" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media">' \
                             + '</iframe>|'
            print(track_markdown, file=rasc_md)
            print('|--|--|--|', file=rasc_md)
    print('\n---\n', file=rasc_md)

rasc_md.close()