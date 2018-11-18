import argparse
import os
import re

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
images_path = os.path.join(root_dir, 'images')

command_description = """
    Rasc utility to remove 'a' and 'b' suffixes from rasc thumbnail files after manual review.
"""

argparser = argparse.ArgumentParser(description=command_description)

argparser.add_argument('-i', '--images-path',
                        dest='images_path',
                        default=images_path,
                        help='Path to Rasc-generated thumbnail PNG files')

with os.scandir(images_path) as images:
    [os.replace(image.path, re.sub(r'[a|b].png', '.png', image.path)) for image in images]
