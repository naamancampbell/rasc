import json
import os
import re
import sys

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
rasc_path = os.path.join(root_dir, 'rasc.txt')
rasc_file = open(rasc_path, 'rU', encoding='utf-8')

rasc_dict = { 'seasons': [] }
season_index = -1
episode_index = -1
track_index = -1
previous_blank = False

for line in rasc_file:
    line = line.strip()
    if line == '':
        previous_blank = True
        continue
    season_match = re.search(r'Season \d+', line)
    if season_match:
        season_title = line
        season = { season_title: [] }
        season_index += 1
        episode_index = -1
        rasc_dict['seasons'].append(season)
        continue
    if previous_blank:
        episode_title = line
        episode = { episode_title: [] }
        episode_index += 1
        track_index = -1
        rasc_dict['seasons'][season_index][season_title].append(episode)
        previous_blank = False
        continue
    no_music_match = re.search(r'No.*music.', line)
    if no_music_match:
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title].append({'no_music': line})
        continue
    track_match = re.search(r'^(\w.*) by (.*)\. (\([\d\w\W]*\))', line)
    if track_match:
        # tracks with movements
        track_index += 1
        track_dict = {
            'title': track_match.group(1),
            'movement': track_match.group(3),
            'artist': track_match.group(2)
        }
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title].append(track_dict)
        continue
    track_match = re.search(r'^(\w.*) by (.*)\.', line)
    if track_match:
        track_index += 1
        track_dict = {
            'title': track_match.group(1),
            'artist': track_match.group(2)
        }
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title].append(track_dict)
        continue
    if line == 'Title card.':
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['time'] = '00:00'
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['scene'] = line
        continue
    segment_match = re.search(r'^\[(.*)\] \((\d+:\d+)\) (.*)', line)
    if segment_match:
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['segment'] = segment_match.group(1)
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['time'] = segment_match.group(2)
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['scene'] = segment_match.group(3)
        continue
    scene_match = re.search(r'^\((\d+:\d+)\) (.*)', line)
    if scene_match:
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['time'] = scene_match.group(1)
        rasc_dict['seasons'][season_index][season_title][episode_index]\
            [episode_title][track_index]['scene'] = scene_match.group(2)
        continue
    # line does not match patterns
    print(
        'Line did not match expected format: {}'.format(line), file=sys.stderr)
    sys.exit(1)

print(json.dumps(rasc_dict, indent=2))
rasc_file.close()
