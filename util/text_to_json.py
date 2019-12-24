import json
import os
import re
import sys

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
rasc_path = os.path.join(root_dir, 'data', 'rasc.txt')
rasc_file = open(rasc_path, 'r', encoding='utf-8')

rasc_dict = { 'seasons': [] }
season_index = -1
episode_index = -1
track_index = -1
previous_blank = False
catalogues = False

for line in rasc_file:
    line = line.strip()
    if line == '':
        previous_blank = True
        catalogues = False
        continue
    if line == 'Catalogues:':
        catalogues = True
        rasc_dict['catalogue_sources'] = []
        continue
    thumbnails_match = re.search(r'Thumbnails: (.*)', line)
    if thumbnails_match:
        rasc_dict['thumbnail_source'] = thumbnails_match.group(1)
        continue
    if catalogues:
        catalogue_match = re.search(r'(.*) \| (.*)', line)
        catalogue = {
            'title': catalogue_match.group(1),
            'url': catalogue_match.group(2)
        }
        rasc_dict['catalogue_sources'].append(catalogue)
        continue
    season_match = re.search(r'Season (\d+)', line)
    if season_match:
        season_index += 1
        episode_index = -1
        season = { 'season': int(season_match.group(1)) }
        season['episodes'] = []
        rasc_dict['seasons'].append(season)
        continue
    if previous_blank:
        episode_index += 1
        track_index = -1
        episode = { 'episode': episode_index + 1 }
        episode['episode_title'] = line
        episode['tracks'] = []
        rasc_dict['seasons'][season_index]['episodes'].append(episode)
        previous_blank = False
        continue
    no_music_match = re.search(r'No.*music.', line)
    if no_music_match:
        rasc_dict['seasons'][season_index]['episodes'][episode_index]\
            ['tracks'].append({'no_music': line})
        continue
    track_match = re.search(r'^(\w.*) by (.*)\. (\([\d\w\W]*\))', line)
    if track_match:
        # tracks with movements
        track_index += 1
        track_dict = {
            'track': track_index + 1,
            'title': track_match.group(1),
            'movement': track_match.group(3),
            'artist': track_match.group(2)
        }
        rasc_dict['seasons'][season_index]['episodes'][episode_index]\
            ['tracks'].append(track_dict)
        continue
    track_match = re.search(r'^(\w.*) by (.*)\.', line)
    if track_match:
        track_index += 1
        title = track_match.group(1)
        artist = track_match.group(2)
        notes_match = re.search(r'^(.*) (\(.*\))', title)
        if notes_match:
            track_dict = {
                'track': track_index + 1,
                'title': notes_match.group(1),
                'notes': notes_match.group(2),
                'artist': artist
            }
        else:
            track_dict = {
                'track': track_index + 1,
                'title': title,
                'artist': artist
            }
        rasc_dict['seasons'][season_index]['episodes'][episode_index]\
            ['tracks'].append(track_dict)
        continue
    scene_match = re.search(
        r'^(?:\[(.*)\] )?\((\d+:\d+)\) \[(\d+:\d+)\] (?:\((t\d+c\d+)\) )?(.*)',
        line)
    if scene_match:
        if scene_match.group(1):
            rasc_dict['seasons'][season_index]['episodes'][episode_index]\
                ['tracks'][track_index]['segment'] = scene_match.group(1)
        rasc_dict['seasons'][season_index]['episodes'][episode_index]\
            ['tracks'][track_index]['dvd_time'] = scene_match.group(2)
        rasc_dict['seasons'][season_index]['episodes'][episode_index]\
            ['tracks'][track_index]['vlc_time'] = scene_match.group(3)
        if scene_match.group(4):
            rasc_dict['seasons'][season_index]['episodes'][episode_index]\
                ['tracks'][track_index]['vlc_location'] = scene_match.group(4)
        rasc_dict['seasons'][season_index]['episodes'][episode_index]\
            ['tracks'][track_index]['scene'] = scene_match.group(5)
        continue
    # line does not match patterns
    print(
        'Line did not match expected format: {}'.format(line), file=sys.stderr)
    sys.exit(1)

rasc_json = os.path.join(root_dir, 'data', 'rasc.json')
with open(rasc_json, 'w') as json_file:
    json.dump(rasc_dict, json_file, indent=2)
rasc_file.close()
