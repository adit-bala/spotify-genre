import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from json.decoder import JSONDecodeError
from flask import Flask, session, request, redirect
from flask_session import Session
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

# Get username from terminal
# username = sys.argv[1]

@app.route('/')
def index():

    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read',
                                               cache_handler=cache_handler,
                                               show_dialog=True)

    if request.args.get("code"):
        # Step 2. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 1. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 3. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return f'<h2>Hi {spotify.me()["display_name"]}, ' \
           f'<small><a href="/sign_out">[sign out]<a/></small></h2>' \
           f'<a href="/genres">my top genres</a> | ' \
        f'<a href="/current_user">me</a>' \



@app.route('/current_user')
def current_user():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


@app.route('/sign_out')
def sign_out():
    session.pop("token_info", None)
    return redirect('/')

@app.route('/genres')
def get_top_genres():
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    auth_manager = spotipy.oauth2.SpotifyOAuth(cache_handler=cache_handler)
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_top_tracks(time_range='long_term', limit=50)


def get_top_genres(timeline, tracks=True):
    time_range, time_description = timeline
    top_genres = get_top_tracks(
        time_range) if tracks else get_top_artists(time_range)
    based = "Songs" if tracks else "Artists"
    print(
        f"Top Genres from the past {time_description} Based on {based} Listened to")
    for i, item in enumerate(top_genres.most_common(10)):
        print(i+1, item[0])
    print()


def get_top_tracks(time_range):
    top_tracks = Counter()
    results = sp.current_user_top_tracks(time_range=time_range, limit=50)
    for item in results['items']:
        artist_id = item['artists'][0]['id']
        artist = sp.artist(artist_id)
        top_tracks.update(artist['genres'])
    return top_tracks


def get_top_artists(time_range):
    top_artists = Counter()
    results = sp.current_user_top_artists(time_range=time_range, limit=50)
    for artist in results['items']:
        top_artists.update(artist['genres'])
    return top_artists


# # Erase cache and prompt for user permission
# try:
#     token = util.prompt_for_user_token(username, scope) # add scope
# except (AttributeError, JSONDecodeError):
#     os.remove(f".cache-{username}")
#     token = util.prompt_for_user_token(username, scope) # add scope

# # Create our spotify object with permissions
# sp = spotipy.Spotify(auth=token)
# ranges = [('short_term', '4 Weeks'), ('medium_term', '6 Months'), ('long_term', 'Several Years')]

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=int(os.environ.get("PORT",
                                                                   os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))
