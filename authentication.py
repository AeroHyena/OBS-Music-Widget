import spotipy
from spotipy.oauth2 import SpotifyPKCE

from decouple import config
import json


global user
user = {}

# Let users give access to their third-party account information via authentication
# Spotify
def spotify_start():
    # Set the scope
    scope = config('SCOPE')
    print("Scope set: " + scope)
            
    # Initiate a global spotify object
    global spotify
    spotify = spotipy.Spotify(auth_manager=SpotifyPKCE(scope=scope, open_browser=True))
    user = spotify.current_user()
    print("The following spotify account has been connected: " + str(user["display_name"]))


    