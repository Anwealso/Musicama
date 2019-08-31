import spotipy
import spotipy.util as util

LEFT = "LEFT"
RIGHT = "RIGHT"

def handle_swipe(track_uri: str, direction: str, playlist_uri: str,
        device_id=None):
    user_id = spotipy.current_user()['id']
    if direction == RIGHT:
        # User liked song
        spotipy.user_playlist_add_tracks(user_id, playlist_uri, [track_uri])
    # Play next song
    spotipy.next_track(device_id=device_id)
    # Return new track information
    return spotipy.currently_playing()

