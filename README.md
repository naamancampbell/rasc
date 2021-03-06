# rasc
Rasc automates the creation of interactive soundtrack websites.<br>
The project is named after the first website created with rasc, the [Ren and Stimpy classical music](https://rasc.netlify.com/) project.

## Getting Started
These instructions detail how to prepare source files for processing into a Hugo-based static website.

### Prerequisites
Install the following programs via package manager eg. `chocolatey`/`apt-get`/`homebrew` (Windows/Ubuntu/Mac):
```
git
python (version 3)
hugo
vlc
```

Install the Spotify Python API package: 
```
pip install spotipy
```
A Spotify Developer account (and App) is required to use `rasc`, sign up at:
https://developer.spotify.com/dashboard

Once registered, set the following environment variables from your new Spotify Application Dashboard (Spotify username can be viewed via https://www.spotify.com/account/overview/):
```
SPOTIPY_CLIENT_ID="1234567890abcdef1234567890abcdef"
SPOTIPY_CLIENT_SECRET="1234567890abcdef1234567890abcdef"
SPOTIPY_REDIRECT_URI="https://example.com/rasc/"
SPOTIPY_USERNAME="123abcdefghijklmnopqrstuv"
```

### Installing
Clone the repository to your PC: 
```
git clone git@github.com:naamancampbell/rasc.git
```

## Source File - data/rasc.txt
The `rasc.txt` file contains the season/episode/track details to generate scene thumbnails and Spotify media for the soundtrack webpages.  The file is converted into JSON format using the following syntax:

### Thumbnails
Summary/title of source media (eg. DVD) used to generate scene thumbnails.
```
Thumbnails: <summary/title>
```
**Example:**<br>
`Thumbnails: The Ren & Stimpy Show: The First and Second Seasons - UNLEASHED (DVD)`

### Catalogues
List (one per line) of websites used to source soundtrack information followed by a blank line.  Catalogue lines are separated into `<title> | <url>` entries.
```
Catalogues:
<title 1> | <url 1>
<title 2> | <url 2>
<blank line>
```
**Example:**<br>
`Catalogues:`<br>
`Toonzone - Music of Ren and Stimpy (via archive.org) | https://web.archive.org/web/20101109014427/http://toonzone.net/wiki/index.php/Music_of_Ren_and_Stimpy
`

### Seasons
Seasons appear before and after a blank line with the `Season N` format, where N is the season number.
```
<blank line>
<Season N>
<blank line>
```
**Example:**<br>
`Season 1`

## Generate JSON file - util/text_to_json.py
Run from the `util` directory to generate the `rasc.json` file from the source `rasc.txt` file.
No arguments required.

## Retrieve Spotify data - util/spotify_data.py
Run from the `util` directory to update the `rasc.json` file with artist image and track URLs from Spotify.
Can be run without arguments or with `--create-playlist "<Playlist Name>"` to generate Spotify playlist.  See Prerequisites section of README for environment variable details.

## Generate thumbnails - util/vlc_thumbs.py
Using vlc, thumbnails are generated as per the rasc JSON file from the source VLC media (eg. DVD).
When run from the `util` directory with no arguments, the `vlc_thumbs.py` uses the following defaults:

```bash
--rasc-json ../data/rasc.json
--vlc-path 'C:\Program Files\VideoLAN\VLC\vlc.exe'
--vlc-mrl dvdsimple:///e:/
--first-title 2
--thumbs-path C:\vlc_thumbs
--season 1
--episode-start 1
--episode-finish 12
--episodes-per-title 2
```

Further details on script arguments can be found via `--help`:
```bash
python vlc_thumbs.py --help
```

Three thumbnails per scene are generated to provide alternative images when undesired captures (blurred, mistimed, etc) are generated.
The thumbnail directory needs to be manually reviewed after generating thumbnails to delete 2 out of the 3 scene thumbnails.
Once the undesired thumbnails have been deleted, run the next script to rename all thumbnails.

## Rename thumbnails - util/rename_thumbs.py
Run from the `util` directory to move the selected thumbnail files to the `rasc/images`
No arguments required.

## Customised Hugo - Newsprint Theme
### Content posts
Season markdown files are required to provide metadata to Hugo layouts.  Season filenames need to be created with the following format: `season-<season_number>.md`.
Within each season markdown file, the following front-matter format is required:
```markdown
---
title: "Season 1"
season_num: 1
publishdate: 2018-11-19T10:58:22.081900+10:00
releasedate: 1991-08-11T21:00:00.000000-05:00
thumbnail: "/s01e01t01.png"
draft: false
---
```
`releasedate` refers to the movie/TV show release date and is displayed under each season on the index page.
The `thumbnail` path refers to the root of the `images` directory.

### Season pages
Season pages are generated by the customised `single.html` layout located in `layouts/_default`.
The layout iterates through the `seasons` JSON item in `data/rasc.json` to display each track, scene and composer/artist.

### Index page
The `index.html` page, located in `themes/newsprint/layouts` has been simplified to suit the project layout.

### Header/Footer partials
The header and footer partials, located in `themes/newsprint/layouts/partials` have been customised to simplify navigation links.
The footer also includes attribution of source thumbnails, catalogue details, and includes links to the generated Spotify playlist.
#### Spotify Code for Playlist
Generating Spotify Codes is a manual process with no API access currently available.
Codes can be generated using https://spotifycodes.com and the resulting JPEG/PNG can be added to the `images` directory.

## Hugo hosting
The Ren and Stimpy Classical project is hosted by Netlify.
The Netlify Large Files service is currently used to host the `images` directory.