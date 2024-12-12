#USE pygetwindow library to get the necessary coordinates of an application to overlay. In this case Terminal
#USE PyQt5 to render and customize the overlay on the desired application.

"""
~~~~~~~Tasks~~~~~~~
From pyget functionality: 
- Get active windows
- Find terminal running the player client
- Actively track window coordinates

From PyQt5
- Overlay top right corner of terminal window
- Display metrics: 
> Personal: 
>> Account
>>> Total score
>>> Total games played
>>> Clickable list of previous games (by random number)
>>>> Win/Loss
>>>> Turns played
>>>> Points gained
>>>> Random number
>> Individual game
>>> Game config
>>> Guesses
>>> Guess aid messages
> Overall: 
>> Players online
>> Leaderboard in points per game
>> Leaderboard in total points
>> Broadcast if a player has won or lost
>> Broadcast when a player comes online
- Allow user to toggle between Personal::Account, Personal::Individual game, and Overall

1. Use gw to get all the terminal coordinates.
2. Use PyQt5 and OCR to figure out which window is a player_client and which is a server 
3. Monitor server window activity to create a matching between client_id (upon connection) and a window
4. For all player client windows open load the proper account information from directory.json
5. Create display overlay on player client windows
6. Display proper personal stats
7. Implement toggle-able actions between personal and global game information
"""

import pygetwindow as gw
import PyQt5

def get_terminal_coordinates():
    all_windows = gw.getAllTitles()
    print(all_windows)

get_window_coordinates()
