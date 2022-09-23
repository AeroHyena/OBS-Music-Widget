# This file manages the music widget - it controls the
# Flask Server, as well as all APIs used to implement 
# functionality that involves third party music streaming services

from types import NoneType
from flask import Flask, render_template
from flask_sock import Sock

import sys
import time
sys.path.append('../OBS_Music_Widget/server/static')

import spotipy
import server.static.spotify as spotify
import config


# Setup the flask server and a sock class
app = Flask(__name__)
sock = Sock(app)


# Widget page
@app.route("/")
def owo():
    return render_template("layout.html")


# Establish a websocket connection between the page and the server using a flask-sock route
@sock.route("/update")
def update(sock):
    
    # Push initial data to the widget
    sock.send(config.__artists__ + ";" + config.__song__)
    
    # Initialize an infinite loop to track player changes on the user's spotify account
    while True:

        # Check if a new song has played
        new_song = spotify.spotify_update(service, config.__song__)

        if new_song:

            # Push an update to the widget
            sock.send(config.__artists__ + ";" + config.__song__)
            print("New song detected - pushing widget update")

        # Wait a second
        time.sleep(1)


# Start the flask server, thereby enabling the widget and its proceses
def start_widget(self):
    app.run()

    

