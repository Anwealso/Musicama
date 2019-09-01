import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
import authenticate
import pprint
from random import shuffle
<<<<<<< HEAD

username = 'mmishr23'
token = authenticate.get_token(username)
sp = authenticate.create_user(token)

=======
import sys
>>>>>>> 01fad60dab59d9eb03f8bd4b9e8b51ded537729e

#Connect to the best playlist, like ever
# playlist_id = 'playlist'
# playlist = sp.user_playlist(username,playlist_id)

def user_playlist_tracks_full(spotify_connection, user, playlist_id=None, fields=None, market=None):
    """ Get full details of the tracks of a playlist owned by a user.
        https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/

        Parameters:
            - user - the id of the user
            - playlist_id - the id of the playlist
            - fields - which fields to return
            - market - an ISO 3166-1 alpha-2 country code.
    """

    # first run through also retrieves total no of songs in library
    response = spotify_connection.user_playlist_tracks(user, playlist_id, fields=fields, limit=100, market=market)
    results = response["items"]

    # subsequently runs until it hits the user-defined limit or has read all songs in the library
    while len(results) < response["total"]:
        response = spotify_connection.user_playlist_tracks(
            user, playlist_id, fields=fields, limit=100, offset=len(results), market=market
        )
        results.extend(response["items"])
    return results

# import pprint
# playlists = sp.user_playlists('spotify')
#
# pprint.pprint(plalists)['items']
#
# def spotify_playlists():
#     response = sp.user_playlists('spotify', offset=0)
#     results = []
#     for elements in response["items"]:
#         results.append(elements)
#     amount = 0
#     while len(results) < 1454:
#         amount +=1
#         response = sp.user_playlists('spotify', offset=(amount*50))
#         for elements in response["items"]:
#             results.append(elements)
#     return results
#
#
# USER_PLAYLISTS = spotify_playlists()
# def parse():
#     for elements in USER_PLAYLISTS:
#         if elements['name'] == 'dw-c':
#             print(elements['uri'])
# parse()
#


<<<<<<< HEAD
def spotify_top_played():
=======
def get_top_tracks(sp):
>>>>>>> 01fad60dab59d9eb03f8bd4b9e8b51ded537729e
    response = sp.current_user_top_tracks()
    results = []
    for elements in response["items"]:
        results.append(elements['uri'])
    amount = 0
    while (len(results)) < 50:
        amount +=1
        response = sp.current_user_top_tracks(offset=(amount*20))
        for elements in response["items"]:
            results.append(elements['uri'])
    return results

<<<<<<< HEAD

def get_recommendations():
    top_tracks = spotify_top_played()
    recommendations = sp.recommendations(seed_tracks=shuffle(top_tracks)[:5],
                                         limit=100)
=======
def generate_seed_tracks(candidate_tracks, limit=5):
    shuffle(candidate_tracks)
    return candidate_tracks[:limit]

def get_recommendations(sp, seed_tracks):
    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=100)
>>>>>>> 01fad60dab59d9eb03f8bd4b9e8b51ded537729e
    recom = []
    for elements in recommendations['tracks']:
        recom.append(elements)
    return recom

<<<<<<< HEAD
recom = get_recommendations()
print(recom)
# for elements in sp.recommendations(
# seed_tracks=spotify_top_played()):
#     print(elements)
=======

    
>>>>>>> 01fad60dab59d9eb03f8bd4b9e8b51ded537729e
