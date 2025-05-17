from spotipy.oauth2 import SpotifyOAuth
import spotipy
import re
import logging
#TODO
# - documentation
# - add volume control
# - fix resume playback


class Plugin:
    def __init__(self,*args,**kwargs):
        client_id = kwargs["client_id"]
        client_secret = kwargs["client_secret"]
        redirect_uri = kwargs["redirect_uri"]
        logging.info("loading Spotify plugin")
        self.scope = "user-read-playback-state,user-modify-playback-state"
        self.sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_uri,
                                                scope=self.scope))
        self.rpi_device_id = None
        devices = self.sp.devices()

        for device in devices['devices']:
            if "raspberry" in device['name'].lower():
                self.rpi_device_id = device['id']
                break

        if self.rpi_device_id is None:
            logging.error("No Raspberry Pi device found")
        else:
            logging.info(f"Raspberry Pi device found: {self.rpi_device_id}")
            # Play on the Raspberry Pi
            self.sp.transfer_playback(self.rpi_device_id,force_play=False)
        logging.info("Spotify plugin loaded")

    def process(self,text):
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
        if text in ["pause","stop","pause musik","pause musik abspielen"] or "musik aus" in text:
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
