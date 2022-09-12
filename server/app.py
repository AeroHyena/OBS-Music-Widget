# This file manages the music widget - it controls the
# Flask Server, as well as all APIs used to implement 
# functionality that involves third party music streaming services

from flask import Flask
import eventlet
from eventlet import wsgi



# Setup the flask server
app = Flask(__name__)


@app.route("/")
def owo():
    return "<p> OWO </p>"








# Start the flask server, thereby enabling the widget and its proceses
def start_widget():
    wsgi.server(eventlet.listen(('', 5000)), app)
    




