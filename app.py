import flask
import authenticate
import time
from models import Musicama

app = flask.Flask(__name__)
token = None
session = None

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/ajax/get_token', methods=['POST'])
def get_token():
    global token
    token = authenticate.get_token(Musicama.USERNAME)
    return token

@app.route('/ajax/start_playback', methods=['GET', 'POST'])
def start_playback():
    time.sleep(3)
    global session
    session = Musicama(auth=token)
    currently_playing = session.init_playback()
    return flask.jsonify(currently_playing)
    
@app.route('/ajax/toggle_playback', methods=['POST'])
def toggle_playback():
    currently_playing = session.toggle_play()
    return flask.jsonify(currently_playing)

@app.route('/ajax/handle_feedback/like', methods=['POST'])
def handle_like():
    currently_playing = session.handle_feedback(Musicama.LIKE)
    return flask.jsonify(currently_playing)

@app.route('/ajax/handle_feedback/dislike', methods=['POST'])
def handle_dislike():
    currently_playing = session.handle_feedback(Musicama.DISLIKE)
    return flask.jsonify(currently_playing)