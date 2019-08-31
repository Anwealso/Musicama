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
    control_playback.toggle_play(session)
    return ""

@app.route('/ajax/handle_feedback/like', methods=['POST'])
def handle_like():
    control_playback.handle_feedback(control_playback.LIKE, session)