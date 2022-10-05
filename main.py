""" This file sets up the app as a tangible window with buttons, layouts, styling and text
The app's Kivy components are defined primarily in the obsmusicwidget.kv file, with Kivy-related 
logic implemented within this file.
Other app functionalities are implemented via seperate .py files. """

# When reffering to widgets, a widget = Kivy widgets and music_widget = the actual widget being outputted

## Imports
# Kivy modules + setup
import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.config import Config

kivy.require("2.1.0")
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

# Other modules
import sys
import os
from os import path
import decouple

# Import app files
from server.app import start_widget, stop_widget
import server.static.spotify as Spotify
import config



## Setup the various modules and variables used in this file
# Setup a log where console output is stored
log = open('log.txt', 'w')
sys.stdout = log
sys.stderr = log
# new_environ = os.environ.copy()


# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = decouple.config('SPOTIFY_CLIENT_ID')
os.environ['SPOTIPY_CLIENT_SECRET'] = decouple.config('SPOTIFY_CLIENT_SECRET')
os.environ['SPOTIPY_REDIRECT_URI'] = decouple.config('REDIRECT')



# Define the different screens/windows of the app, and a manager for the screens
class Controller(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connected_accounts = {}
        self.spotify_action = "Connect"
        self.connect_status = "No account connected"
        self.get_accounts()
        print(self.spotify_action)

    # Keep track of connected accounts
    def get_accounts(self):
        if path.exists(".cache"):
            spotify_user_data = Spotify.username(config.spotify_start(self))
            print(spotify_user_data)
            self.connected_accounts.update({"spotify_account": spotify_user_data["display_name"]})
            self.spotify_action = "Disconnect"
            self.connect_status = self.connected_accounts["spotify_account"]
            
        
    ## enable starting and stopping the widget

    def start(self):
        # Check if any accounts are connected
        if len(self.connected_accounts) < 1:
            print("No accounts are connected!")
            return
        
        start_widget(int(decouple.config('PORT')))
        print("The widget is successfully launched (initiated via button id='start_widget_button')")

    def stop(self):
        stop_widget()
        print("The widget is successfully shut down (initiated via button id='stop_widget_button'")

    def restart(self):

        # Stop widget
        stop_widget()

        # Start widget
        start_widget()
        print("The widget is successfully restarted (initiated via button id='restart_widget_button')")


    


class Customize(Screen):
    pass


# Customize screen tab pages
class Visuals(Screen):
    pass


class Behavior(Screen):
    pass


# Other screens

class Guide(Screen):
    pass


class SettingsPage(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class CustomizeTabManager(ScreenManager):
    pass


# Base sidebar button parent class
class SidebarButton(Button):
    pass

# Setup the entire app as a class that inherits from Kivy's App class
class OBSMusicWidgetApp(App):
    pass




# On app launch
if __name__ == "__main__":
    # Start the app
    OBSMusicWidgetApp().run()
    print("The app is now active")
    
