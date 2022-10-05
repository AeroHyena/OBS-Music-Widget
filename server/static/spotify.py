# This scripts contains all the spotify functions used by the widget
# Authentication is handled via config.py in the root directory

import config

import time
import sys
sys.path.append('../OBS_Music_Widget')

import requests
import shutil 


# Get username of the connected account
def username(spotify):
    username = spotify.current_user()
    return username


# Get the user's current playback
def get_playback(spotify):
    data = spotify.current_playback()
    print("Grabbed user playback data")
    return data


# Check the user's current playing song, and push an update to the widget if a new song is playing
def spotify_update(spotify, previous):

    # Get the user's current playback
    print(spotify)
    data = get_playback(spotify)
    # print(data)
    
    # Check if an ad is playing
    # Ads last 15-30 secs
    if data["currently_playing_type"] == "ad":
        time.sleep(8)
        return

    # Check is a new song is playing
    if not data:
        pass
    
    song = data["item"]["name"]
    if song != previous:

        # Get the cover image and save it to static
        image = data["item"]["album"]["images"][0]["url"]
        print("Grabbing image link - " + str(image))

        get_image = requests.get(image, stream = True)
        image_file = open("server/static/image.jpg",'wb')
        shutil.copyfileobj(get_image.raw, image_file)
        print("Cover image saved")
        image_file.close()

        # Update artists names
        artists = ""

        if len(data["item"]["album"]["artists"]) > 1:

            for i, item in enumerate(data["item"]["album"]["artists"]):
                artists += str(data["item"]["album"]["artists"][i]["name"])

                if len(data["item"]["album"]["artists"]) != i + 1:
                    artists += ", "

        else:
            artists = data["item"]["album"]["artists"][0]["name"]

        # Save song and artists details to config.py
        config.__song__ = song
        config.__artists__ = artists 

        return True

    else:
        return False


                