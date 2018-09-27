import json
import os
import re

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
rasc_path = os.path.join(root_dir, 'rasc.txt')
rasc_file = open(rasc_path, 'rU', encoding='utf-8')

rasc_dict = { 'seasons': [] }
season = 'Season 1'
previous_blank = False

for line in rasc_file:
    if line == '':
        previous_blank = True
        continue
    match = re.search(r'Season \d+', line)
    if match:
        season = { line.strip(): [] }
        rasc_dict['seasons'].append(season)
        continue

print('Rasc dict: {}'.format(rasc_dict))
rasc_file.close()
