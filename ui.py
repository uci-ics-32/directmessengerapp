# James Homer
# jphomer@uci.edu
# 14782048

# ui.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

from pathlib import Path
import a6


MSG_ERROR = '\nERROR\n'

MSG_WELCOME = 'Welcome to PyJournal\nEnter Q to stop the program. Enjoy!\n'
INP_WELCOME = 'Here are your options:\n1. Create a new Profile\n2. Open an existing Profile\n'

MSG_CREATE = '\nEnter profile information (to skip, leave blank unless required)\n'
MSG_CREATE2 = '\nProfile created.\n'
INP_CREATE_SERVER = '\nWhat DSP server would you like to connect to?\n'
INP_CREATE_USER = '\nWhat username would you like to use? (required)\n'
INP_CREATE_PASS = '\nWhat password would you like to use? (required)\n'
INP_CREATE_BIO = '\nEnter a brief bio:\n'
INP_CREATE_PATH = '\nWhere will your profile be stored? (enter a valid path)\n'
INP_CREATE_NAME = '\nWhat would you like to name your profile?\n'

MSG_OPEN = '\nProfile loaded\n'
INP_OPEN_PATH = '\nEnter the location of the existing profile (enter a valid path):\n'

MSG_MAINMENU = 'Main menu\nWhat would you like to do next?\n'
MSG_MAINMENU_OPTIONS = '1. Create a new Profile\n2. Open an existing Profile\n3. Edit an existing Profile\n4. Add a journal entry\n5. Delete a journal entry\n6. Print\n7. Post an entry online\n'
INP_MAINMENU_4 = "\nWhat would you like to post?\nUse '@weather' to get a weather description\nUse '@lastfm' to print a top track with its artist\nUse '@extracredit' to get a Nasa article title.\n"
INP_MAINMENU_5 = '\nWhat is the index of the post you would like to delete?\n'
INP_MAINMENU_7 = '\nWhich post would you like to publish online (enter id)?\n'

INP_ACCOUNT_USER = "What will your username be?\n"
INP_ACCOUNT_PASS = "What will your password be?\n"
INP_ACCOUNT_BIO = "What do you want to include in your bio?\n"

MSG_EDITMENU = '\nWhat would you like to edit?\n1. Username\n2. Password\n3. Bio\n'
INP_EDITMENU_USER = '\nWhat would you like your new username to be?\n'
INP_EDITMENU_PASS = '\nWhat would you like your new password to be?\n'
INP_EDITMENU_BIO = '\nWhat would you like your new bio to be?\n'

MSG_EDIT_DELPOST = '\nPost successfully deleted.\n'
MSG_EDIT_DELPOST2 = 'Invalid index.'

MSG_PRINTMENU = '\nWhat would you like to print?\n1. Username\n2. Password\n3. Bio\n4. Every post\n5. Specific post\n6. All information'
INP_PRINTMENU_5 = '\nWhat is the index of the post you would like to print?\n'


def create_ui():
    print(MSG_CREATE)
    store_p = input(INP_CREATE_PATH)
    dsp_server = input(INP_CREATE_SERVER)
    name1 = input(INP_CREATE_NAME)
    path1 = Path(store_p)
    path1 = path1 / (name1 + '.dsu')
    if path1.exists():
        a6.openj(path1)
    user1 = input(INP_CREATE_USER)
    while ' ' in user1:
        print(MSG_ERROR)
        user1 = input(INP_CREATE_USER)
    pass1 = input(INP_CREATE_PASS)
    while ' ' in pass1:
        print(MSG_ERROR)
        pass1 = input(INP_CREATE_PASS)
    bio1 = input(INP_CREATE_BIO)
    return dsp_server, user1, pass1, bio1, store_p, name1


def main_menu_ui():
    print(MSG_MAINMENU)
    print(MSG_MAINMENU_OPTIONS)


def edit_menu_ui():
    print(MSG_EDITMENU)


def print_menu_ui():
    print(MSG_PRINTMENU)

