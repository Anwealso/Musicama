import spotipy
import datetime
import get_tracks
import time

DEVICE_NAME = "Musicama"

class Musicama(spotipy.Spotify):

    PLAYLIST_NAME = "Musicama Liked Songs"
    RECOM_PLAYLIST_NAME_PREFIX = "Musicama Recommendations "
    USERNAME = 'byronho24'
    SEED_LIMIT = 5

    DISLIKE = "LEFT"
    LIKE = "RIGHT"

    
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
        # print(playlist_all_data)
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
        top_tracks = get_tracks.get_top_tracks(self)
        # print('successfully got top tracks, len %d' % (len(top_tracks),))
        seed_tracks = get_tracks.generate_seed_tracks(top_tracks)
        # print('successfully got seed tracks, len %d' % (len(seed_tracks),))
        self.recommended_tracks = get_tracks.get_recommendations(self, seed_tracks)
        # print('successfully got recommended tracks, len %d' % (len(recommended_tracks),))
        # Put new recommendations into playlist
        self.user_playlist_add_tracks(self.username, self.recom_playlist_id, 
                [track['uri'] for track in self.recommended_tracks])
        # Liked tracks by user
        self.liked_tracks = []
        # Current playlist offset
        self.current_offset = 0
        # Is playing
        self.is_playing = False

    def add_to_liked_tracks(self, track_uri):
        self.liked_tracks.append(track_uri)
        self.user_playlist_add_tracks(self.username, self.likes_playlist_id,
                [track_uri])

    def get_new_recommendations(self):
        # Remove old recommendations
        self.user_playlist_remove_all_occurrences_of_tracks(
            self.username, self.recom_playlist_id, 
                    [track['uri'] for track in self.recommended_tracks]
        )
        # Get new recommendations
        self.recommended_tracks = get_tracks.get_recommendations(self, self.liked_tracks)
        # Liked tracks were used as seed - reset liked tracks
        self.liked_tracks = []
        # Put new recommendations into playlist
        self.user_playlist_add_tracks(self.username, self.recom_playlist_id, 
                [track['uri'] for track in self.recommended_tracks])
        # Reset current offset
        self.current_offset = 0

    @staticmethod
    def get_track_metadata(currently_playing_data):
        artists = []
        for artist in currently_playing_data['item']['artists']:
            artists.append(artist['name'])
        artists = ", ".join(artists)
        track_title = currently_playing_data['item']['name']
        album_art = currently_playing_data['item']['album']['images'][0]['url']
        print(currently_playing_data['is_playing'])
        data = {
            'album_art': album_art,
            'track_title': track_title,
            'artist_name': artists,
            'is_playing': currently_playing_data['is_playing']
        }

    def get_currently_playing_track_data(self):
        current_track = self.recommended_tracks[self.current_offset]
        artists = []
        for artist in current_track['artists']:
            artists.append(artist['name'])
        artists = ", ".join(artists)
        track_title = current_track['name']
        album_art = current_track['album']['images'][0]['url']
        data = {
            'album_art': album_art,
            'track_title': track_title,
            'artist_name': artists,
            'is_playing': self.is_playing,
            'uri': current_track['uri']
        }
        return data

    def handle_feedback(self, swipe_feedback: str):
        current_track_uri = self.get_currently_playing_track_data()['uri']
        self.current_offset += 1
        if swipe_feedback == Musicama.LIKE:
            # User liked song
            self.add_to_liked_tracks(current_track_uri)
            if len(self.liked_tracks) == Musicama.SEED_LIMIT:
                self.get_new_recommendations()
                self.init_playback()
            else:
                self.start_playback(
                    device_id=self.device_id,
                    context_uri="spotify:playlist:"+self.recom_playlist_id, 
                    offset={"position": self.current_offset}
                )
        else:
            # Play next song
            self.start_playback(
                    device_id=self.device_id,
                    context_uri="spotify:playlist:"+self.recom_playlist_id, 
                    offset={"position": self.current_offset}
            )
        
        # Return new track information
        time.sleep(1)
        return self.get_currently_playing_track_data() 


    def init_playback(self):
        self.start_playback(
            self.device_id, 
            context_uri="spotify:playlist:"+self.recom_playlist_id, 
            offset={"position": self.current_offset}
        )
        self.is_playing = True
        return self.get_currently_playing_track_data()

    def toggle_play(self):
        if self.is_playing:
            self.pause_playback(device_id=self.device_id)
            self.is_playing = False
        else:
            self.start_playback(device_id=self.device_id)
            self.is_playing = True
        time.sleep(1)
        return self.get_currently_playing_track_data()

    

    