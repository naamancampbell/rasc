import argparse
import os
import re
import shutil

util_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(util_dir)
images_path = os.path.join(root_dir, 'images')

command_description = """
    Rasc utility to remove 'a' and 'b' suffixes 
    from rasc thumbnail files after manual review.
"""

argparser = argparse.ArgumentParser(description=command_description)

argparser.add_argument('-t', '--thumbs-path',
                        dest='thumbs_path',
                        default=r'C:\vlc_thumbs',
                        help='Path to Rasc-generated thumbnail PNG files')

argparser.add_argument('-i', '--images-path',
                        dest='images_path',
                        default=images_path,
                        help='Rasc project path to store renamed thumbnails')

argresults = argparser.parse_args()
thumbs_path = os.path.abspath(argresults.thumbs_path)
images_path = os.path.abspath(argresults.images_path)

if not os.path.exists(images_path):
    os.makedirs(images_path)

with os.scandir(thumbs_path) as images:
    for image in images:
        renamed_image = re.sub(r'[a|b].png', '.png', image.path)
        os.replace(image.path, renamed_image)
        rasc_path = os.path.join(images_path, os.path.basename(renamed_image))
        shutil.move(renamed_image, rasc_path)
