import flask
import control_playback
import authenticate
import time

app = flask.Flask(__name__)
username = 'byronho24'
token = None
session = None

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/ajax/get_token', methods=['POST'])
def get_token():
    global token
    token = authenticate.get_token(username)
    return token

@app.route('/ajax/start_playback', methods=['GET', 'POST'])
def start_playback():
    global session
    if session is None:
        session = authenticate.create_user(token)
    currently_playing = control_playback.toggle_play(session)
    return flask.jsonify(control_playback.get_track_metadata(currently_playing))
    

@app.route('/ajax/handle_feedback/like', methods=['POST'])
def handle_like():
    currently_playing = control_playback.handle_feedback(control_playback.LIKE, session)
    return flask.jsonify(control_playback.get_track_metadata(currently_playing))