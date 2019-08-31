import spotipy
import spotipy.util as util
import authenticate
import sys
from models import Musicama
import time

DISLIKE = "LEFT"
LIKE = "RIGHT"



def handle_feedback(swipe_feedback: str, session: Musicama, playlist_to_add_to=None):
    from pprint import pprint
    pprint(session.currently_playing())
    current_track_uri = session.currently_playing()['item']['uri']
    if playlist_to_add_to is None:
        playlist_all_data = session.user_playlist_create(
            session.user_id, 'Musicama Liked Songs')
        playlist_to_add_to = playlist_all_data['id']
    if swipe_feedback == LIKE:
        # User liked song
        session.user_playlist_add_tracks(session.user_id, playlist_to_add_to, [current_track_uri])
    # Play next songs
    session.next_track(device_id=session.device_id)
    # Return new track information
    return session.currently_playing()

def toggle_play(session):
    current_state = session.currently_playing()
    if current_state and current_state['is_playing']:
        session.pause_playback(device_id=session.device_id)
    else:
        session.start_playback(session.device_id, context_uri="https://open.spotify.com/album/28RiDrxACWNtbrUNy9Ks1X?si=RXbZARreRci7F2bB9TTAFw")
    return

def main():
    username = sys.argv[1]
    token = authenticate.get_token(username)
    print(token)
    input("press enter when ready")
    session = authenticate.create_user(token)
    print(session.device_id)
    # time.sleep(10)
    # handle_feedback(LIKE, session)


if __name__ == "__main__":
    main()