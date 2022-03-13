# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# a6.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

import ds_client
import Profile
from pathlib import Path
import ui
import json
from LastFM import LastFM
from OpenWeather import OpenWeather
from ExtraCreditAPI import Nasa


loaded_path = ''

def start():
    '''Starts the program.'''
    user_inp = input()
    if user_inp == '1':
        create()
    elif user_inp == '2':
        openj()
    elif user_inp == 'admin':
        admin()
    elif user_inp == 'Q':
        quit()
    else:
        print(ui.MSG_ERROR)
        start()


def create():
    '''Creates a new profile.'''         
    dsp_server, user1, pass1, bio1, store_p, name1 = ui.create_ui()
    #Creates the path
    p = Path(store_p)
    #Names the file
    file_name = name1
    if len(file_name) > 1:     
        #Creates the file with the provided name and appends the file type '.dsu'
        p = p / (file_name + '.dsu')
        global loaded_path
        loaded_path = p
        #Finishes initializing the file if it does not already exist
        if not p.exists():
            p.touch()
    #Error-checks for if the name of the file is blank
    else:
        print(ui.MSG_ERROR)
    print(p)
    account(p, dsp_server, user1, pass1, bio1)
    print(ui.MSG_CREATE2)
    main_menu()


def openj(p=None):
    '''Opens an existing profile.'''
    if p == None:
        store_p = input(ui.INP_OPEN_PATH)
    else:
        store_p = p
    #Creates the path
    p = Path(store_p)
    global loaded_path
    loaded_path = p
    if p.exists() and p.suffix == '.dsu':
        with open(p) as f:
            try:
                line = f.readline()
                json.loads(line)
            except:
                print(ui.MSG_ERROR)
                print(ui.INP_WELCOME)
                start()
        profile = Profile.Profile('')
        profile.load_profile(p)
        print(ui.MSG_OPEN)
        main_menu()
    #Error-checks in case the file does not exist
    else:
        print(ui.MSG_ERROR)
        openj()


def post_online(num_post):
    '''Posts an entry online for the selected profile.'''
    profile = Profile.Profile('')
    profile.load_profile(loaded_path)
    for index, post in enumerate(profile.get_posts()):
        if index == num_post:
            ds_client.send(profile.dsuserver, 3021, profile.username, profile.password, post['entry'], profile.bio)


def main_menu():
    '''Provides the user with the functionalities of the program.'''
    ui.main_menu_ui()
    choice = input()
    if choice == '1':
        create()
    elif choice == '2':
        openj()
    elif choice == '3':
        edit_menu(loaded_path)
    elif choice == '4':
        post = input(ui.INP_MAINMENU_4)
        cmd = '-addpost' + ' "' + post + '"'
        edit(cmd, loaded_path)
        main_menu()
    elif choice == '5':
        post = input(ui.INP_MAINMENU_5)
        cmd = '-delpost' + ' ' + post
        edit(cmd, loaded_path)
        main_menu()
    elif choice == '6':
        print_menu(loaded_path)
        main_menu()
    elif choice == '7':
        post1 = input(ui.INP_MAINMENU_7)
        post_online(int(post1))
        main_menu()
    elif choice == 'Q':
        quit()
    else:
        print(ui.MSG_ERROR)
        main_menu()


def account(file, dsu_server=None, username=None, password=None, bio='', admin=False):
    '''Establishes the account for the user.'''
    if username == None and admin == False:
        username = input(ui.INP_ACCOUNT_USER)
    if password == None and admin == False:
        password = input(ui.INP_ACCOUNT_PASS)
    if bio == '' and admin == False:
        bio = input(ui.INP_ACCOUNT_BIO)
    profile = Profile.Profile('')
    profile.dsuserver = dsu_server
    profile.username = username
    profile.password = password
    profile.bio = bio
    profile.save_profile(file)


def edit_menu(path):
    '''Provides a main menu for the edit ui.'''
    ui.edit_menu_ui()
    inp1 = input()
    if inp1 == '1':
        usr1 = input(ui.INP_EDITMENU_USER)
        while ' ' in usr1:
            print(ui.MSG_ERROR)
            usr1 = input(ui.INP_EDITMENU_USER)
        edit('-usr' + ' "' + usr1 + '"', path)
        main_menu()
    elif inp1 == '2':
        pwd1 = input(ui.INP_EDITMENU_PASS)
        while ' ' in pwd1:
            print(ui.MSG_ERROR)
            pwd1 = input(ui.INP_EDITMENU_PASS)
        edit('-pwd' + ' "' + pwd1 + '"', path)
        main_menu()
    elif inp1 == '3':
        bio1 = input(ui.INP_EDITMENU_BIO)
        edit('-bio' + ' "' + bio1 + '"', path)
        main_menu()
    elif inp1 == 'Q':
        quit()
    else:
        edit_menu(path)


def edit(commands, p):
    '''Edits the user information.'''
    errors = 0
    if '-usr' in commands and errors == 0:
        profile = Profile.Profile('')
        profile.load_profile(p)
        try:
            usernme = commands[commands.index('-usr "') + 6:commands.index('"', commands.index('-usr "') + 6)]
        except:
            usernme = commands[commands.index("-usr '") + 6:commands.index("'", commands.index("-usr '") + 6)]
        if ' ' in usernme:
            print(ui.MSG_ERROR)
            errors += 1
        else:
            profile.username = (usernme)
        profile.save_profile(p)
    if '-pwd' in commands and errors == 0:
        profile = Profile.Profile('')
        profile.load_profile(p)
        try:
            pwd_chg = commands[commands.index('-pwd "') + 6:commands.index('"', commands.index('-pwd "') + 6)]
        except:
            pwd_chg = commands[commands.index("-pwd '") + 6:commands.index("'", commands.index("-pwd '") + 6)]
        if ' ' in pwd_chg:
            print(ui.MSG_ERROR)
            errors += 1
        else:
            profile.password = (pwd_chg)
        profile.save_profile(p)
    if '-bio' in commands and errors == 0:
        profile = Profile.Profile('')
        profile.load_profile(p)
        try:
            bio_chg = commands[commands.index('-bio "') + 6:commands.index('"', commands.index('-bio "') + 6)]
        except:
            bio_chg = commands[commands.index("-bio '") + 6:commands.index("'", commands.index("-bio '") + 6)]
        profile.bio = (bio_chg)
        profile.save_profile(p)
    if '-addpost' in commands and errors == 0:
        profile = Profile.Profile('')
        profile.load_profile(p)
        try:
            word = commands[commands.index('-addpost "') + 10:commands.index('"', commands.index('-addpost "') + 10)]
            #Checks if a keyword is in the post the user typed out, and if so, undergoes transclusion
            try:
                if '@weather' in word:
                    apikey = '63b3bf0aeb696dbac81b065b1f495d0f'
                    obj = OpenWeather("92697", "US")
                    obj.set_apikey(apikey)
                    obj.load_data()
                    word = obj.transclude(word)
                if '@lastfm' in word:
                    apikey = 'e85f8731bd9869562cc8530e60ee1438'
                    obj = LastFM()
                    obj.set_apikey(apikey)
                    obj.load_data()
                    word = obj.transclude(word)
                if '@extracredit' in word:
                    apikey = "vRZYxUeFLKDrwCvJbZ2Om3GH46cElm1qD7QVsLVt"
                    obj = Nasa()
                    obj.set_apikey(apikey)
                    obj.load_data()
                    word = obj.transclude(word)
                post_chg = word
                profile.add_post(Profile.Post(post_chg))
                profile.save_profile(p)
            except Exception:
                print(ui.MSG_ERROR)
        except:
            word = commands[commands.index("-addpost '") + 10:commands.index("'", commands.index("-addpost '") + 10)]
            #Checks if a keyword is in the post the user typed out, and if so, undergoes transclusion
            try:
                if '@weather' in word:
                    apikey = '63b3bf0aeb696dbac81b065b1f495d0f'
                    obj = OpenWeather("92617", "US")
                    obj.set_apikey(apikey)
                    obj.load_data()
                    word = obj.transclude(word)
                if '@lastfm' in word:
                    apikey = 'e85f8731bd9869562cc8530e60ee1438'
                    obj = LastFM()
                    obj.set_apikey(apikey)
                    obj.load_data()
                    word = obj.transclude(word)
                if '@extracredit' in word:
                    apikey = "vRZYxUeFLKDrwCvJbZ2Om3GH46cElm1qD7QVsLVt"
                    obj = Nasa()
                    obj.set_apikey(apikey)
                    obj.load_data()
                    word = obj.transclude(word)
                post_chg = word
                profile.add_post(Profile.Post(post_chg))
                profile.save_profile(p)
            except Exception:
                print(ui.MSG_ERROR)
    if '-delpost' in commands and errors == 0:
        profile = Profile.Profile('')
        profile.load_profile(p)
        delpost_chg = commands[commands.find('-delpost ') + 9: commands.find('-delpost ') + 10]
        if profile.del_post(int(delpost_chg)):
            print(ui.MSG_EDIT_DELPOST)
        else:
            print(ui.MSG_EDIT_DELPOST2)
        profile.save_profile(p)


def print_menu(path):
    '''Provides a ui for the print functionality.'''
    ui.print_menu_ui()
    inp1 = input()
    possible_inp = ['1', '2', '3', '4', '5', '6', 'Q']
    if inp1 == '1':
        print_func('-usr', path)
    if inp1 == '2':
        print_func('-pwd', path)
    if inp1 == '3':
        print_func('-bio', path)
    if inp1 == '4':
        print_func('-posts', path)
    if inp1 == '5':
        post = input(ui.INP_PRINTMENU_5)
        print_func('-post ' + post, path)
    if inp1 == '6':
        print_func('-all', path)
    if inp1 == 'Q':
        quit()
    if inp1 not in possible_inp:
        print_menu(path)


def print_func(commands, p):
    '''Prints out information that the user calls for.'''
    if '-usr' in commands:
        profile = Profile.Profile('')
        profile.load_profile(p)
        print(f'\nUsername: {profile.username}\n')
    if '-pwd' in commands:
        profile = Profile.Profile('')
        profile.load_profile(p)
        print(f'\nPassword: {profile.password}\n')
    if '-bio' in commands:
        profile = Profile.Profile('')
        profile.load_profile(p)
        print(f'\nBio: {profile.bio}\n')
    if '-posts' in commands:
        profile = Profile.Profile('')
        profile.load_profile(p)
        for index, post in enumerate(profile.get_posts()):
            print(f'{index}: {post.entry}\n')
    if '-post ' in commands:
        profile = Profile.Profile('')
        profile.load_profile(p)
        for index, post in enumerate(profile.get_posts()):
            if index == int(commands[commands.find('-post ') + 6: commands.find('-post ') + 10]):
                print(f'{index}: {post.entry}\n')
    if '-all' in commands:
        profile = Profile.Profile('')
        profile.load_profile(p)
        print(f'\nUsername: {profile.username}')
        print(f'Password: {profile.password}')
        print(f'Bio: {profile.bio}')
        print('Posts:\n')
        for index, post in enumerate(profile.get_posts()):
            print(f'{index}: {post.entry}\n')


def admin():
    #This loop will continually ask for input until 'Q' is entered
    while True:
        inp1 = input()
        #If 'Q' is entered, the program ends
        if inp1 == 'Q':
            break
        #If 'C' is entered, a new file is created under the name the user specifies
        elif inp1[0:1] == 'C':
            #Creates the path
            p = Path(inp1[2:inp1.find(' -')])
            file_name = inp1[inp1.find('-n ') + 3:]
            if len(file_name) > 1:
                #Creates the file with the provided name and appends the file type '.dsu'
                p = p / (file_name + '.dsu')
                global loaded_path
                loaded_path = p
                #Finishes creating the file if it does not already exist
                if not p.exists():
                    p.touch()
            #Error-checks for if the name of the file is blank
            else:
                print(ui.MSG_ERROR)
            print(p)
            account(p, admin=True)
            print(ui.MSG_CREATE2)
        #If 'O' is entered, opens/loads the contents of the DSU file
        elif inp1[0:1] == 'O':
            #Creates the path
            p = Path(inp1[2:])
            loaded_path = p
            if p.exists() and p.suffix == '.dsu':
                with open(p) as f:
                    try:
                        line = f.readline()
                        json.loads(line)
                    except:
                        print(ui.MSG_ERROR)
                        continue
                profile = Profile.Profile('')
                profile.load_profile(p)
                print(ui.MSG_OPEN)
            #Error-checks in case the file does not exist
            else:
                print(ui.MSG_ERROR)
                continue
        #If 'E' is entered, allows for editting of the username, password, bio, adding a post, and deleting a post
        elif inp1[0:1] == 'E':
            edit(commands = inp1[2:], p = loaded_path)
        #If 'P' in entered, prints the contents of the DSU file
        elif inp1[0:1] == 'P':
            print_func(commands = inp1[2:], p = loaded_path)
        #Error-checks for if the user either omits the starting command or attempts a starting command that does not exist
        else:
            print(ui.MSG_ERROR)

#Calls the start function, which begins the file explorer, only if this file's name is main
if __name__ == "__main__":
    print(ui.MSG_WELCOME)
    print(ui.INP_WELCOME)
    start()
