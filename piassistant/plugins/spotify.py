from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import spotipy
import re
import logging
import os
import webbrowser
import time
import urllib.parse
import subprocess
from word2num_de import word_to_number


#TODO
# - documentation
# - add volume control


class Plugin:
    def __init__(self,memory, client_id, client_secret,redirect_uri, **kwargs):
        logging.info("loading Spotify plugin")

        # Initialize Spotify client with credentials
        #self.auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.auth_manager = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope="user-read-email user-read-private user-read-playback-state user-modify-playback-state streaming",open_browser=False)

        self.access_token = self.auth_manager.get_access_token(as_dict=False)
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)
        # Start the web player
        self.start_webplayer(self.access_token)
        # Check 10 times if there is a Raspberry Pi device available
        for _ in range(10):
            devices = self.sp.devices()
            if devices['devices']:
                logging.info("active devices found")
                break
            time.sleep(5)
        
        self.rpi_device_id = None
        devices = self.sp.devices()

        for device in devices['devices']:
            if "piassistant Player" == device['name']:
                self.rpi_device_id = device['id']
                break

        if self.rpi_device_id is None:
            logging.error("No piassistant Player device found")
        else:
            logging.info(f"piassistant Player device found: {self.rpi_device_id}")
            # Transfer playback to the web player
            self.sp.transfer_playback(self.rpi_device_id, force_play=False)
        
        logging.info("Spotify plugin loaded")

    def process(self, text):
        #play track
        play_track = re.search(r'spiele (.*)', text)
        if play_track:
            track = play_track.group(1)

            #search for a track
            track_results = self.sp.search(q=track,type="track")
            track = track_results["tracks"]["items"][0]
            self.sp.start_playback(uris=[track["uri"]])

        #play playlist
        play_user_playlist = re.search(r'spiele meine playlist (.*)', text)
        if play_user_playlist:
            playlist = play_user_playlist.group(1)
            #search for a playlist
            playlist_results = self.sp.current_user_playlists()
            for pl in playlist_results["items"]:
                if pl["name"].lower() == playlist.lower():
                    playlist = pl
                    break
            else:
                logging.error(f"Playlist {playlist} not found")
                return
            self.sp.start_playback(context_uri=playlist["uri"])

        #pause playback
        if text in ["pause","stopp","pause musik","pause musik abspielen"] or "musik aus" in text:
            self.sp.pause_playback()

        #resume playback
        if text in ["weiter","weiter spielen","weiter musik","musik weiter"] or "musik an" in text:
            #doesnt start at last track
            self.sp.start_playback()
        
        #next track
        if text in ["nächster","nächster track","weiter track","weiter zum nächsten track"] or "nächster song" in text:
            self.sp.next_track()
        
        #play artist
        play_artist = re.search(r'spiele musik von (.*)', text)
        if play_artist:
            artist = play_artist.group(1)
            #search for a artist
            artist_results = self.sp.search(q=artist,type="artist")
            artist = artist_results["artists"]["items"][0]
            self.sp.start_playback(context_uri=artist["uri"])

        #set volume percentage
        set_volume = re.search(r'lautstärke (.*) prozent', text)
        if set_volume:
            volume = set_volume.group(1)
            try:
                volume = word_to_number(volume)
            except ValueError:
                logging.error(f"Invalid volume: {volume}")
                return
            
            if 0 <= volume <= 100:
                self.sp.volume(volume)
            else:
                logging.error(f"Volume out of range: {volume}")

    def start_webplayer(self, web_sdk_token):
        """
        Opens the Spotify web player with embedded token.
        """
        import tempfile
        import os
        
        # Read the template
        template_file = os.path.join(os.path.dirname(__file__), "player.html")
        
        if not os.path.exists(template_file):
            logging.error(f"Template file not found: {template_file}")
            return
        
        with open(template_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Replace the placeholder with the actual token
        html_content = html_content.replace("{{SPOTIFY_TOKEN}}", web_sdk_token)
        
        # Create a temporary file
        temp_dir = tempfile.mkdtemp()
        temp_html = os.path.join(temp_dir, 'player_temp.html')
        
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Open in browser
        if os.name == 'nt':  # Windows
            file_url = f"file:///{temp_html.replace(os.sep, '/')}"
            webbrowser.open(file_url)
        else:
            logging.info("Running on Linux, starting Xvfb for headless browser support")
            file_url = f"file://{temp_html}"
            # Start Xvfb
            xvfb_process = subprocess.Popen(['Xvfb', ':99', '-screen', '0', '800x600x24'])
            os.environ['DISPLAY'] = ':99'
            time.sleep(2)
            # Open browser with minimal window size
            try:
                subprocess.run(['chromium-browser', '--no-sandbox', '--window-size=640,480', '--autoplay-policy=no-user-gesture-required', file_url], check=True)
            except FileNotFoundError:
                try:
                    subprocess.run(['firefox', '--width=640', '--height=480', file_url], check=True)
                except FileNotFoundError:
                    print("No suitable browser found")
        
        logging.info(f"Opening Spotify player: {file_url}")