
The problem I aim to solve


Livestreaming is a very modern phenomena, bringing with it another layer of online success for content creators, parasocial relationships, etc.

Having been a hobbyist livestreamer in the past, and looking forward to doing so again in the future, I found that, in trying to improve the production qulaity of your content, many streamers seek a method to display information of music playing on their livestreams - a now-playing widget with the song title, artist, etc.

Currently, methods available for achieving this result is not very reliable. Web scrobbling works, but it takes about 1 minute into a osng before the widget is updated to display the new song's information. There are pieces of software other individuals wrote, but these are often either outdated, buggy or requires other third-party softwares to work, which only creates more room for bugs, and eventually leads to a broken widget.


How I went about creating a solution

I decided to build my own app for this, one that has everything that is required for the widget to function in one place. 

My design for the app is to create a control pannel that the user can utilize to control and configure the widget. I want it not only to enable functionality for a now-playing widget, but other functionality that can be added over time, like a music player that can play music from any link proved, and even assemple playlists with songs from different streaming services for example. I decided to use Kivy to create the control panel, whilst using Flask to build a server in which the widget can run.

Initially, my approach to the file layout was to implement the kivy app directly into the flask server itself, but I quickly realized that this will be tricky to do. Where would the kivy file go - in static? templates? How will I launch this app if the file in charge of that is placed in some sub-folder? I ended up seperating the flask server into a seperate folder. It made sense to do so, considering that the kivy file defines a control panel to control the widget, whereas the server is the widget itself.

Starting off with v1.0, utilizing the kivy documentation and YouTube tutorials, I quickly built a test window, establishng the layout of the app early on, and adding a sidebar, I used kivy's screenmanager to allow the window to change to whatever the user selects from the sidebar, and implemented buttons to start, stop and restart the widget/server.

thereafter I implemented the flask server. I intitally struggled to fully implement a start and stop widget functionality, because while flask has an app.run() function. it doesn't have an app.stop() counterpart. I also found that when starting a flask server while kivy is running, the kivy app would be frozen until the server is shut down. I tried many solutions presented online, and in the end I got it to work was by using multiprocessing to start the flask server as a seperate process.

For v1.1 I implemented an authentication module that allows users to connect their 3rd-party accounts to the app, and added spotify functionality via the spotipy module. I created a test app on the spotify developer's portal, and seperated it's keys into a .env file. I also tried to add in the user's authentication data into the .env file knowing that I want to encrypt the .env file in a future version, but I realized that spotipy relies on the base .cache file where user authentication data is stored for it's own functionalities, so I left it as is.

For v1.2 I implemented the visuals of the widget, and extended the spotify functionality so that the widget page is fully-functional, and displays a user's current playback with the song's details and cover image. During this set-up I had a lot of error trying to keep the widget functional during spotify ad playback, and my code was messy from a lot of experimentation, which caused only more issues. After cleaning it up and some extra effort I managed to get everything working smoothly.

At this point I decided to focus the app only on spotify, since Tidal and Apple Music require subscriptions to run, and YouTube depriciated its api's activity list functionality. I ended up converting the authentication.py file I used for connecting user accounts to the app into a config.py file that also manages global variables - one big challenge for me was keeping variables acessible between modules, and I realized that while global variables usually are importable, object variables can only be shared cross-module via function returns.
