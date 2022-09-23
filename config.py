# This module handles connecting the app to a user's spotify account, as well as global variables
import spotipy
from spotipy.oauth2 import SpotifyPKCE

import decouple



# Global Variables
__user__ = {}
__song__ = "-"
__artists__ = "-"


# Start a spotify object to be used in other modules
def spotify_start():

    # Set the scope within which the user's account data will be used
    scope = decouple.config('SCOPE')
    print("Scope set: " + scope)
            
    # Initiate thwspotify object
    spotify = spotipy.Spotify(auth_manager=SpotifyPKCE(scope=scope, open_browser=True))
    print("Spotify is initiated (" + str(spotify) + ")")
    
    # Get the username of the connected account
    user_spotify = spotify.current_user()
    print("The following spotify account has been connected: " + str(user_spotify["display_name"]))

    # Return the object so it can be passed to other modules
    return spotify


    