import spotipy

class SpotifyCtl:

    def __init__(self, auth_manager):
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def next_track(self):
        self.sp.next_track()
