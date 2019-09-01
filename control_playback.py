import spotipy
import spotipy.util as util
import authenticate
import sys
from models import Musicama
import time

DISLIKE = "LEFT"
LIKE = "RIGHT"

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
    return data


def handle_feedback(swipe_feedback: str, session: Musicama):
    current_track_uri = session.currently_playing()['item']['uri']
    if swipe_feedback == LIKE:
        # User liked song
        session.user_playlist_add_tracks(session.user_id, session.likes_playlist_id, [current_track_uri])
    # Play next songs
    session.next_track(device_id=session.device_id)
    # Return new track information
    time.sleep(1)
    return session.currently_playing()

def toggle_play(session):
    current_state = session.currently_playing()
    if current_state and current_state['is_playing']:
        session.pause_playback(device_id=session.device_id)
    else:
        session.start_playback(session.device_id, context_uri="https://open.spotify.com/album/54FblbvyHNrWeAuEJqnyit")
    time.sleep(1)
    return session.currently_playing()

def main():
    username = sys.argv[1]
    token = authenticate.get_token(username)
    # print(token)
    input("press enter when ready")
    session = authenticate.create_user(token)
    # print(session.device_id)
    # time.sleep(10)
    # handle_feedback(LIKE, session)


if __name__ == "__main__":
    main()