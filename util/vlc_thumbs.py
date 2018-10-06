import argparse
import json
import os
from subprocess import call

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
rasc_path = os.path.join(root_dir, 'data', 'rasc.json')

command_description = """
    Rasc utility to capture thumbnails from media using VLC.
    Uses Rasc-generated JSON files to determine scenes to capture.
"""

argparser = argparse.ArgumentParser(description=command_description)

argparser.add_argument('-j', '--rasc-json',
                        dest='rasc_path',
                        default=rasc_path,
                        help='Path to Rasc-generated JSON file')

argparser.add_argument('-p', '--vlc-path',
                        dest='vlc_path',
                        default=r'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe',
                        help='Path to VLC executable/binary')

argparser.add_argument('-m', '--vlc-mrl',
                        dest='vlc_mrl',
                        default='dvd:///e:/',
                        help='Path to VLC MRL (media location) - eg. dvd:///e:/')

argparser.add_argument('-f', '--first-title',
                        dest='vlc_title',
                        default=2,
                        help='First title (in VLC) episodes start from')

argparser.add_argument('-t', '--thumbs-path',
                        dest='thumbs_path',
                        default=r'C:\vlc_thumbs',
                        help='Path to output generated thumbnails')

argparser.add_argument('-s', '--season',
                        dest='media_season',
                        default=1,
                        help='Season to process on current media')

argparser.add_argument('-S', '--episode-start',
                        dest='episode_start',
                        default=1,
                        help='Starting episode to process on current media')

argparser.add_argument('-F', '--episode-finish',
                        dest='episode_end',
                        default=12,
                        help='Finishing episode to process on current media')

argparser.add_argument('-e', '--episodes-per-title',
                        dest='eps_per_title',
                        default=2,
                        help='Number of episodes per VLC title on current media')

argresults = argparser.parse_args()

rasc_path = argresults.rasc_path
vlc_path = argresults.vlc_path
vlc_mrl = argresults.vlc_mrl
vlc_title = argresults.vlc_title - 1
thumbs_path = argresults.thumbs_path
media_season = argresults.media_season
episode_start = argresults.episode_start
episode_end = argresults.episode_end
eps_per_title = argresults.eps_per_title

if not os.path.exists(thumbs_path):
    os.makedirs(thumbs_path)

def get_sec(time_str):
    # Source: https://stackoverflow.com/a/6402859/8751739
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)    

with open(rasc_path, 'r') as f:        
    rasc_json = json.load(f)

for season_index, season in enumerate(rasc_json['seasons'], start=1):
    if season_index == media_season:
        season_title = list(season.keys())[0]
        for episode_index, episode in enumerate(season[season_title], start=1):
            if episode_index in list(range(episode_start, episode_end + 1)):
                episode_title = list(episode.keys())[0]
                if eps_per_title == 1 or (episode_index % eps_per_title) != 0:
                    vlc_title += 1            
                for track_index, track in enumerate(episode[episode_title], start=1):
                    if track.get('no_music'):
                        continue
                    scene_image = 's' + '%02d' % season_index \
                                + 'e' + '%02d' % episode_index \
                                + 't' + '%02d' % track_index
                    track_start = get_sec(track['time'])
                    call([vlc_path, vlc_mrl + '#' + str(vlc_title), '--rate=1', '--video-filter=scene', '--vout=dummy', '--start-time=' + str(track_start), '--stop-time=' + str(track_start + 1), '--scene-format=png', '--scene-ratio=24', '--scene-prefix=' + scene_image, '--scene-path=' + thumbs_path, '--scene-replace', 'vlc://quit'])
                    call([vlc_path, vlc_mrl + '#' + str(vlc_title), '--rate=1', '--video-filter=scene', '--vout=dummy', '--start-time=' + str(track_start + 2), '--stop-time=' + str(track_start + 3), '--scene-format=png', '--scene-ratio=24', '--scene-prefix=' + scene_image + 'a', '--scene-path=' + thumbs_path, '--scene-replace', 'vlc://quit'])
                    call([vlc_path, vlc_mrl + '#' + str(vlc_title), '--rate=1', '--video-filter=scene', '--vout=dummy', '--start-time=' + str(track_start + 4), '--stop-time=' + str(track_start + 5), '--scene-format=png', '--scene-ratio=24', '--scene-prefix=' + scene_image + 'b', '--scene-path=' + thumbs_path, '--scene-replace', 'vlc://quit'])
