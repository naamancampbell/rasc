# rasc
Rasc automates the creation of interactive soundtrack websites.<br>
The project is named after the first website created with rasc, the Ren and Stimpy classical music project.

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

Once registered, set the following environment variables from your new Spotify Application Dashboard (Spotify username can be viewed via  https://www.spotify.com/account/overview/):
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

