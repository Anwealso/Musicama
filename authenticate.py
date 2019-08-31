import sys
import spotipy
import spotipy.util as util
from models import Musicama

client_id = '468ecf32cd4d416e806d0a3e8153080f'
client_secret = 'f94cad73e4d643aba1480a349429ffab'
redirect_uri = 'https://localhost:8008/'

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read' + \
        ' streaming user-modify-playback-state user-read-currently-playing ' + \
        'user-read-playback-state user-read-email user-read-private'

def get_token(username):
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, \
            redirect_uri)
    return token

def create_user(token):
    sp = Musicama(auth=token)
    return sp


def main():
    username = sys.argv[1]
    token = get_token(username)
    sp = create_user(token)
    print(token)

if __name__ == "__main__":
    main()