import json
import os
import sys
import unittest

from util.vlc_thumbs import create_argparser, generate_thumbs

class TestRasc(unittest.TestCase):

    def setUp(self):
        self.argparser = create_argparser()

    def test_vlc_thumbs_sequential(self):
        # Source: https://archive.org/details/DishonoredLadyDVDiso
        args = self.argparser.parse_args([
            '--vlc-mrl', 'dvd:///c:/Temp/Dishonored_Lady.iso',
            '--vlc-path', r'C:\Program Files\VideoLAN\VLC\vlc.exe',
            '--first-title', 1])
