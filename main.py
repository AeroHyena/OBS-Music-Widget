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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config
from kivy.clock import Clock
from kivy.metrics import dp

kivy.require("2.1.0")
Config.set('graphics', 'width', '1000')
Config.set('graphics', 'height', '600')

# Other modules
import sys
import os
import decouple
import dotenv
import spotipy

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
port = decouple.config('PORT')




# Define the different screens/windows of the app, and a manager for the screens
class Controller(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connected_accounts = {}
        self.spotify_action = "Connect"
        self.connect_status = "No account connected"
        self.get_accounts()
        

    # Keep track of connected accounts 
    def get_accounts(self):
        if os.path.exists(".cache"):
            spotify_user_data = Spotify.username(config.spotify_start())
            self.connected_accounts.update({"spotify_account": spotify_user_data["display_name"]})
            self.spotify_action = "Disconnect"
            self.connect_status = self.connected_accounts["spotify_account"]

        
    def spotify_account_manage(self, button):
        # If an account is connected, remove it and update the widgets
        if os.path.exists(".cache"):
            os.remove(".cache")
            self.connected_accounts = {}
            print("Disconnected spotify account")

            button.parent.children[1].text = "No account connected"
            button.text = "Connect"

        # If no account is connected, connect the user's account
        else:
            # Set the scope within which the user's account data will be used
            scope = decouple.config('SCOPE')
            print("Scope set: " + scope)
                    
            # Initiate the spotify object
            spotify = spotipy.Spotify(auth_manager=spotipy.SpotifyPKCE(scope=scope, open_browser=True))
            print("Spotify is initiated (" + str(spotify) + ")")
            
            # Get the username of the connected account
            user_spotify = spotify.current_user()
            print("The following spotify account has been connected: " + str(user_spotify["display_name"]))

            # Update connected accounts info
            button.parent.children[1].text = user_spotify["display_name"]
            button.text = "Disconnect"
            self.connected_accounts.update({"spotify_account": user_spotify["display_name"]})


    # Change server status bar to reflect server activity
    def server_listener(self, state):
        global port 
        
        if state == "Inactive":
            self.children[0].children[3].children[2].children[0].text = state
            self.children[0].children[3].children[2].children[0].color = (1, 0, 0, 1)
        else:
            self.children[0].children[3].children[2].children[0].text = state + f" on localhost:{port}"
            self.children[0].children[3].children[2].children[0].color = (0, 1, 0, 1)

        print(f"The server is {state}")
        

    ## enable starting and stopping the widget

    def start(self):
        # Check if any accounts are connected
        if len(self.connected_accounts) < 1:
            print("No accounts are connected!")

            # Popup on no account connected
            box = BoxLayout(orientation="vertical")
            box.add_widget(Label(text='Please connect your account via the section below the widget controls box'))
            dismiss = Button(text="Ok", size_hint=(None, None), height=dp(30), width=dp(100))
            box.add_widget(dismiss)

            accounts_popup = Popup(title="No accouunt is connected!", 
            content=box,
            auto_dismiss=False)

            dismiss.bind(on_press=accounts_popup.dismiss)
            accounts_popup.open()
            return

        # Start the widget
        self.server_listener("Active")
        start_widget(int(port))
        print("The widget is successfully launched")

        # Disable self and enable other buttons
        # Start
        self.children[0].children[3].children[0].children[2].disabled=True 

        # Stop
        self.children[0].children[3].children[0].children[1].disabled=False
        
        # Restart
        self.children[0].children[3].children[0].children[0].disabled=False


    def stop(self):
        stop_widget()
        self.server_listener("Inactive")
        print("The widget is successfully shut down")

        # Disable self and enable other buttons
        # Start
        self.children[0].children[3].children[0].children[2].disabled=False

        # Stop
        self.children[0].children[3].children[0].children[1].disabled=True
        
        # Restart
        self.children[0].children[3].children[0].children[0].disabled=True

    def restart(self):

        # Stop widget
        stop_widget()

        # Start widget
        start_widget(int(decouple.config('PORT')))
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

    def save_settings(self):
        # Get the new port
        global port
        port  = self.children[0].children[0].children[2].children[1].text

        # Save the new port 
        dotenv.set_key(".env", "PORT", port, quote_mode='never')
        print("New port set: " + port)


class WindowManager(ScreenManager):
    pass


class CustomizeTabManager(ScreenManager):
    pass


# Base sidebar button parent class
class SidebarButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.after_init, 1)

    # On launch, set all buttons opacity to 0.5 except for the Controller button
    def after_init(self, dt):
        if self.text != "Controller":
            self.opacity = 0.5

    def change_active_window(self):
        # Set all buttons opacity to 0.5
        for button in self.parent.children:
            button.opacity = 0.5

        # Then set own opacity to 1
        self.opacity = 1


# Base tab button parent class
class TabButton(Button):
    
    def change_active_tab(self):
        # Set all tabs color to the base dark blue
        for tab in self.parent.children:
            tab.background_color = (0, 0, 0, 1)

        # Set self to the lighter blue
        self.background_color = (3 / 255, 76 / 255, 130 / 255, 1)

# Setup the entire app as a class that inherits from Kivy's App class
class OBSMusicWidgetApp(App):
    pass




# On app launch
if __name__ == "__main__":
    # Start the app
    print("The app is now active")
    OBSMusicWidgetApp().run()
    print("The app is now closed.")
    
    
