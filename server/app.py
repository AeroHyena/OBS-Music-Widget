# This file manages the music widget - it controls the
# Flask Server, as well as all APIs used to implement 
# functionality that involves third party music streaming services

from flask import Flask
import eventlet
from eventlet import wsgi
import spotipy
import os.path


"""
# Get user acess token
f = open(os.path.dirname(__file__) + '/../.cache')
x = f.read()
x = x.replace('"access_token": ', '')
f.close()

token = ''
quotes = 0

for letter in range(len(x)):
    if x[letter] == '{':
        continue
    if quotes == 2:
        break
    if x[letter] == '"':
        quotes += 1
        continue
    token = token + x[letter]

print(token)






sp = spotipy.Spotify(auth=token)
"""

# Setup the flask server
app = Flask(__name__)


@app.route("/")
def owo():
    return "<p> OWO </p>"



def test(spotify):
    # Some test code 
    results = spotify.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " - ", track['name'])








# Start the flask server, thereby enabling the widget and its proceses
def start_widget():
    wsgi.server(eventlet.listen(('', 5000)), app)
    




