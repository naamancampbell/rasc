import json
import os
from subprocess import call

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
rasc_path = os.path.join(root_dir, 'data', 'rasc.json')
vlc_path = 'C:\Program Files (x86)\VideoLAN\VLC\vlc.exe'
vlc_title = 1

def get_sec(time_str):
    # Source: https://stackoverflow.com/a/6402859/8751739
    m, s = time_str.split(':')
    return int(m) * 60 + int(s)    

with open(rasc_path, 'r') as f:        
    rasc_json = json.load(f)

for season_index, season in enumerate(rasc_json['seasons'], start=1):
    season_title = list(season.keys())[0]
    for episode_index, episode in enumerate(season[season_title], start=1):
        episode_title = list(episode.keys())[0]
        if (episode_index % 2) != 0:
            vlc_title += 1            
        for track_index, track in enumerate(episode[episode_title], start=1):
            if track.get('no_music'):
                continue
            scene_image = 's' + '%02d' % season_index \
                        + 'e' + '%02d' % episode_index \
                        + 't' + '%02d' % track_index
            track_start = get_sec(track['time'])
            call([vlc_path, 'dvd:///e:/#' + str(vlc_title), '--rate=1', '--video-filter=scene', '--vout=dummy', '--start-time=' + str(track_start), '--stop-time=' + str(track_start + 1), '--scene-format=png', '--scene-ratio=24', '--scene-prefix=' + scene_image, '--scene-path=C:\vlcsnaps', '--scene-replace', 'vlc://quit'])