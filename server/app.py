# This file manages the music widget - it controls the
# Flask Server, as well as all APIs used to implement 
# functionality that involves third party music streaming services

# Flask modules
from flask import Flask, render_template
from flask_sock import Sock
import eventlet
from eventlet import wsgi

# Other modules + setup
import sys
import os
from os import path
import time
from multiprocessing import Process, freeze_support

sys.path.append('../OBS_Music_Widget/server/static')

# Api and config files
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

    # Get the appropriate api
    api = activcate_apis()
    
    # Push initial data to the widget
    sock.send(config.__artists__ + ";" + config.__song__)
    
    # Initialize an infinite loop to track player changes on the user's spotify account
    while True:

        # Check if a new song has played
        new_song = spotify.spotify_update(api, config.__song__)

        if new_song:

            # Push an update to the widget
            sock.send(config.__artists__ + ";" + config.__song__)
            print("New song detected - pushing widget update")

        # Wait a second
        time.sleep(1)


# Flask server setup
def start_server(port):
    wsgi.server(eventlet.listen(('', port)), app)


# Start the flask server as a seperate process, 
# thereby enabling the widget and its proceses
def start_widget(port):
    global server
    server = Process(target=start_server, args=(port,))
    server.daemon = True
    server.start()


# Terminate the server process
def stop_widget():
    global server
    server.terminate()


# Activate api services
# Setup of this function assumes that more apis will be added in the future, in which
# case only the user's service of choce's api will be activated
def activcate_apis():
    spotify = config.spotify_start()
    return spotify

    

