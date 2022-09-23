# This file sets up the app as a tangible window with buttons, layouts, styling and text
# The app's Kivy components are defined primarily in the obsmusicwidget.kv file, with few functionalities partially implemented within this file
# Other functionalities are implemented via seperate .py files



import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

import sys
import os
from os import path
from multiprocessing import Process
import decouple

from server.app import start_widget
from config import spotify_start



# Setup the various modules used in this file
kivy.require("2.1.0")
log = open('log.txt', 'w')
sys.stdout = log
sys.stderr = log
# new_environ = os.environ.copy()


# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = decouple.config('SPOTIFY_CLIENT_ID')
os.environ['SPOTIPY_CLIENT_SECRET'] = decouple.config('SPOTIFY_CLIENT_SECRET')
os.environ['SPOTIPY_REDIRECT_URI'] = decouple.config('REDIRECT')


# Activate api services on app start
def activcate_apis():
    if path.exists(".cache"):
        print(".cache exists: " + str(path.exists(".cache")))
        spotify = spotify_start()
        return spotify


# Define the different screens/windows of the app, and a manager for the screens
class Controller(Screen):
    
    # enable starting and stopping the widget
    def start(self):
        if not path.exists(".cache"):
            print("No accounts are connected!")
            return

        global p1
        p1 = Process(target=start_widget)
        p1.daemon = True
        p1.start()
        print("The widget is successfully launched (initiated via button id='start_widget_button')")

    def stop(self):
        global p1
        p1.terminate()
        print("The widget is successfully shut down (initiated via button id='stop_widget_button'")

    def restart(self):

        # Stop widget
        global p1
        p1.terminate()

        # Start widget
        p1 = Process(target=start_widget)
        p1.daemon = True
        p1.start()
        print("The widget is successfully restarted (initiated via button id='restart_widget_button')")


class Customize(Screen):
    pass


class Guide(Screen):
    pass

class SettingsPage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# Setup the entire app as a class that inherits from Kivy's App class
class OBSMusicWidgetApp(App):
    pass


# On app launch
if __name__ == "__main__":
    global api 
    api = activcate_apis()

    # Start the app
    print("The app is now active")
    OBSMusicWidgetApp().run()
    
