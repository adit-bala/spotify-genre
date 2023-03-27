import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from json.decoder import JSONDecodeError
from collections import Counter

# Get username from terminal
username = sys.argv[1]
scope = 'user-top-read'


# abstract to get genres from artists and tracks at the same time
def get_top_genres(time_range='long_term'):
    top_genres = Counter()
    results = sp.current_user_top_tracks(time_range=time_range, limit=50)
    for item in results['items']:
        artist_id = item['artists'][0]['id']
        artist = sp.artist(artist_id)
        top_genres.update(artist['genres']) 
    print(time_range.upper())
    for i, item in enumerate(top_genres.most_common(10)):
        print(i+1, item[0])
    print()


# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permissions
sp = spotipy.Spotify(auth=token)
ranges = ['short_term', 'medium_term', 'long_term']
for rng in ranges:
    get_top_genres(rng)




