import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from json.decoder import JSONDecodeError
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

# Get username from terminal
username = sys.argv[1]
scope = 'user-top-read'


def get_top_genres(timeline, tracks=True):
    time_range, time_description = timeline 
    top_genres = get_top_tracks(time_range) if tracks else get_top_artists(time_range)
    based = "Songs" if tracks else "Artists"
    print(f"Top Genres from the past {time_description} Based on {based} Listened to")
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


# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permissions
sp = spotipy.Spotify(auth=token)
ranges = [('short_term', '4 Weeks'), ('medium_term', '6 Months'), ('long_term', 'Several Years')]
for rng in ranges:
    get_top_genres(rng)