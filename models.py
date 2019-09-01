import spotipy
import datetime
import get_tracks

DEVICE_NAME = "Musicama"

class Musicama(spotipy.Spotify):

    PLAYLIST_NAME = "Musicama Liked Songs"
    RECOM_PLAYLIST_NAME_PREFIX = "Musicama Recommendations "
    USERNAME = 'byronho24'
    SEED_LIMIT = 5
    
    @staticmethod
    def get_device(session: spotipy.Spotify):
        # print(session.devices())
        # TODO: need to guess the device id of the web player?
        devices = session.devices()['devices']
        # print(devices)
        for device in devices:
            if device['name'] == 'Web Playback SDK Quick Start Player':
            # if device['name'] == 'ONEPLUS A5010':
                return device['id']

    @staticmethod
    def find_likes_playlist(session: spotipy.Spotify):
        for playlist in session.current_user_playlists()['items']:
            if playlist['name'] == Musicama.PLAYLIST_NAME:
                return playlist['id']
        return None

    @staticmethod
    def create_playlist(session: spotipy.Spotify, name: str):
        playlist_all_data = session.user_playlist_create(
                session.me()['id'], name)
        return playlist_all_data['id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_id = Musicama.get_device(self)
        self.user_id = self.me()['id']
        self.username = Musicama.USERNAME
        # Initialise playlist where the liked tracks are stored
        likes_playlist_id = Musicama.find_likes_playlist(self)
        if likes_playlist_id is None:
            likes_playlist_id = Musicama.create_playlist(
                self, Musicama.PLAYLIST_NAME)
        self.likes_playlist_id = likes_playlist_id
        # Initialise playlist to store temporary recommendations
        self.recom_playlist_id = Musicama.create_playlist(self, 
                Musicama.RECOM_PLAYLIST_NAME_PREFIX + \
                    datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S"))
        # Get initial recommendations
        self.recommended_tracks = get_tracks.get_recommendations(
            self, get_tracks.generate_seed_tracks(get_tracks.get_top_tracks(self))
        )
        # Liked tracks by user
        self.liked_tracks = []

    def add_to_liked_tracks(self, track_uri):
        self.liked_tracks.append(track_uri)
        if len(self.liked_tracks) == Musicama.SEED_LIMIT:
            self.get_new_recommendations()
        self.user_playlist_add_tracks(self.username, self.likes_playlist_id,
                [track_uri])

    def get_new_recommendations(self):
        # Remove old recommendations
        self.user_playlist_remove_all_occurrences_of_tracks(
            self.username, self.recom_playlist_id, self.recommended_tracks
        )
        # Get new recommendations
        self.recommended_tracks = get_tracks.get_recommendations(self, self.liked_tracks)
        # Liked tracks were used as seed - reset liked tracks
        self.liked_tracks = []
        # Put new recommendations into playlist
        self.user_playlist_add_tracks(self.username, self.recom_playlist_id, self.recommended_tracks)    
    

    