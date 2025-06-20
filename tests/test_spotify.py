import context
from piassistant.plugins.spotify import Plugin
import unittest
import time


class TestSpotifyPlugin(unittest.TestCase):
    def setUp(self):
        client_id="id"
        client_secret="secret"
        redirect_uri="uri"
        self.plugin = Plugin(None,client_id=client_id, client_secret=client_secret,redirect_uri=redirect_uri)
    
    def test_play_track(self):
        # Test playing a track
        text = "spiele weiß der geier"
        self.plugin.process(text)
        # Check if the track is playing
        playback = self.plugin.sp.current_playback()
        self.assertIsNotNone(playback)
        time.sleep(0.5)
        self.assertEqual(playback['is_playing'], True)

    def test_play_artist(self):
        # Test playing an artist
        text = "spiele musik von george ezra"
        self.plugin.process(text)
        # Check if the artist is playing
        playback = self.plugin.sp.current_playback()
        self.assertIsNotNone(playback)
        self.assertEqual(playback['is_playing'], True)

    def test_pause_playback(self):
        # Test pausing playback
        text = "pause"
        self.plugin.process(text)
        # Check if playback is paused
        playback = self.plugin.sp.current_playback()
        self.assertIsNotNone(playback)
        self.assertEqual(playback['is_playing'], False)
