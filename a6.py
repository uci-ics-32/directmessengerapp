# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# a6.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP direct messaging program.

from cmath import e
from ctypes import alignment
from pickle import TRUE
import tkinter as tk
from tkinter import E, Toplevel, ttk, filedialog
from turtle import right, width
from Profile import Profile
from Profile import Messages
from ds_messenger import DirectMessenger
import time


'''
A custom exception class that is called when a profile's messages are attempted to be loaded, 
but the profile does not have any messages yet.
'''
class NoMessages(Exception):
    pass

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Message objects available in the active DSU file
        self.messages = [Messages]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        global index_global
        index = int(self.posts_tree.selection()[0])
        index_global = index
        # Updates the msg_box with the messages for the selected recipient/conversation
        self.insert_msg_box()
    

    def insert_msg_box(self):
        '''Updates the msg_box with the messages for the selected recipient/conversation'''
        messages = self.messages[index_global]['messages']
        # Allows for editting of the textbox
        self.msg_box.configure(state=tk.NORMAL)
        self.msg_box.delete(0.0, 'end')
        for message in messages:
            # Determines whether the message is sent by the user or received -- used for determining alignment in the message box
            if message['from'] == 'you':
                self.msg_box.insert(tk.END, message['message'] + '\n') 
            else:
                self.msg_box.tag_configure('tag-right', justify='right')
                self.msg_box.insert(tk.END, message['message'] + '\n', 'tag-right')
        # Disables editting of the textbox
        self.msg_box.configure(state=tk.DISABLED)
    

    """
    Returns the text that is currently displayed in the entry_editor widget.
    """
    def get_text_entry(self) -> str:
        return self.entry_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """
    def set_text_entry(self, text:str):
        #deletes all current text in the self.entry_editor widget
        self.entry_editor.delete(0.0, 'end')   # delete between two indices, 0-based
        #inserts the value contained within the text parameter
        self.entry_editor.insert(0.0, text)   # insert new text at a given index
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_messages(self, messages:list):
        '''Populates self._posts with the post data passed in the posts parameter 
        and repopulates the UI with the new post entries'''
        self.messages = messages
        # Repopulates the UI with the new post entries
        for index, message in enumerate(self.messages):
            self._insert_post_tree(index, message['recipient'])

    """
     Inserts a single post to the post_tree widget.
    """
    def insert_post(self, recipient):
        self.messages.append(recipient)
        id = len(self.messages) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, recipient)


    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        '''Fully resets the UI to a clean slate.'''
        self.set_text_entry("")
        self.msg_box.configure(state=tk.DISABLED)
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, recipient):
        entry = recipient
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."
        
        self.posts_tree.insert('', id, id, text=entry)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_frame = posts_frame
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        # Creates the outer frame for the messages box
        msgs_frame = tk.Frame(master=self, bg="")
        msgs_frame.pack(fill=tk.BOTH, side=tk.TOP)
        self.msgs_frame = msgs_frame

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP)
        self.entry_frame = entry_frame

        # Creates the inner frame for the messages box
        msg_frame = tk.Frame(master=msgs_frame, bg="green")
        msg_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=5)
        self.msg_frame = msg_frame

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=5)
        self.editor_frame = editor_frame

        # Creates the textbox for the user to send posts
        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        # Creates the textbox that is not user-changable for the messages
        self.msg_box = tk.Text(master=msg_frame, width=0, height=21)
        self.msg_box.configure(state=tk.DISABLED)
        self.msg_box.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        # Creates a scroll frame and scrollbar
        scroll_frame = tk.Frame(master=msg_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        msg_box_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.msg_box.yview)
        self.msg_box['yscrollcommand'] = msg_box_scrollbar.set
        msg_box_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        
        self.root = root
        self._send_callback = send_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets.
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._send_callback is not None:
            self._send_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        # Creates a send button that will take the user-typed message and sends it to the server
        send_button = tk.Button(master=self, text="Send", width=20)
        send_button.configure(command=self.save_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)
        self.send_button = send_button

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""
class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root

        # Creates a profile object that keeps track of the user's profile information
        self._current_profile = Profile()

        self._current_profile.dsuserver = '168.235.86.101'
        self._current_profile.username = 'vanillamilkshake'
        self._current_profile.password = 'yum'
        self._current_profile.bio = 'mybio'

        # Creates class version frames for later editting of the dark mode
        self.entry_frame = None
        self.editor_frame = None
        self.save_button = None
        self.entry_edit = None

        # Creates a dm object that is used to send messages over the server to other users
        self.dm = DirectMessenger(self._current_profile.dsuserver, self._current_profile.username, self._current_profile.password)

        self._profile_filename = None

        self.add_window = None
        self.add_entry_edit = None
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self.profile_filename = filename.name

        self._current_profile.dsuserver = '168.235.86.101'
        self._current_profile.username = 'vanillamilkshake'
        self._current_profile.password = 'yum'
        self._current_profile.bio = 'mybio'
        self._current_profile.save_profile(self.profile_filename)
        self.body.reset_ui()
    
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        self._profile_filename = filename.name
        self._current_profile = Profile()
        # Loads the current user's profile
        self._current_profile.load_profile(self._profile_filename)

        # Resets the UI for the new loaded profile
        self.body.reset_ui()

        # Sets the loaded user's messages for the UI
        self.body.set_messages(self._current_profile.get_messages())
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def send_msg(self):
        # Retrieves the user-typed in text from the entry box
        text = self.body.get_text_entry()

        # Retrieves the recipient for the message
        recipient = self.body.messages[index_global]['recipient']

        # Sends the message with the recipient over the server
        self.dm.send(text, recipient)

        # Adds the message to the local files to keep track of the message log locally offline
        self._current_profile.add_message(Messages(recipient, {"from": 'me', "message": text, "timestamp": time.time()}))
        #Adds the post to the profile and saves it locally
        self._current_profile.save_profile(self._profile_filename)
        #Resets the UI text box
        self.body.set_text_entry("")

        self.body.insert_msg_box()


    def save_add(self):
        '''Saves the username and password and then closes the window'''
        self._save_add()
        # Closes the window after the button is save button is pressed
        self.add_window.destroy()
    
    def _save_add(self):
        '''Saves any changes to the settings'''
        try:
            # Retrieves the recipient
            user = self.add_entry_edit.get(1.0, 2.0).rstrip()
            recipient = user[user.index('"') + 1:-1]
            # Entries must be between the double quotes
            self._current_profile.add_message(Messages(recipient))
            self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
            # After a new user is added, the conversation is added to the treeview
            for index, message in enumerate(self.body.messages):
                self.body._insert_post_tree(index, message['recipient'])
        except Exception as e:
            print(e)
            print('Username error. Make sure input is between double quotes and that a profile is active!')


    def add_user(self):
        '''Allows the user to add a user recipient for their profile when the 'Add User' menu item is clicked'''
        # Creates a new Toplevel window that will allow for changing of the username and password
        add_usr = Toplevel()
        self.add_window = add_usr
        # Titles the new window
        add_usr.title("Add User")
        # Sets the size of the new windows
        add_usr.geometry("360x280")
        add_usr.minsize(add_usr.winfo_width(), add_usr.winfo_height())

        # Creates an entry and editor frame that the user can type in and add a user/recipient to their contacts
        entry_frame = tk.Frame(master=add_usr, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.entry_frame = entry_frame
        editor_frame = tk.Frame(master=self.entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.editor_frame = editor_frame
        
        # Creates a button widget that saves the new user/recipient that the user added
        save_button = tk.Button(master=editor_frame, text="Add User", width=20)
        save_button.configure(command=self.save_add)
        save_button.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        self.save_button = save_button

        # Creates a text widget that allows for editing of recipient
        entry_edit = tk.Text(editor_frame, width=0)
        entry_edit.pack(fill=tk.X, side=tk.TOP, expand=True, padx=5, pady=5)
        self.entry_edit = entry_edit

        # Clears the text box for later use
        entry_edit.delete(0.0, 'end')
        # Inserts the value contained of the current recipient
        entry_edit.insert(0.0, f'Enter the recipient\'s username: ""')

        self.add_entry_edit = entry_edit


    def dark_mode_on(self):
        '''Turns the widgets to a darker grey per the user's click on the setting'''
        self.root.config(bg='#000000')
        self.footer.root.config(bg='#676767')
        self.footer.send_button.config(bg='#676767')
        self.body.entry_editor.config(bg='#676767')
        self.body.msg_box.config(bg='#676767')
        self.body.posts_frame.config(bg='#676767')
        self.body.msgs_frame.config(bg='#676767')
        self.body.entry_frame.config(bg='#676767')
        self.body.msg_frame.config(bg='#676767')
        self.body.editor_frame.config(bg='#676767')


    def dark_mode_off(self):
        '''Turns the widgets back to the normal colors per the user's click on the setting'''
        self.root.config(bg='SystemButtonFace')
        self.footer.root.config(bg='SystemButtonFace')
        self.footer.send_button.config(bg='SystemButtonFace')
        self.body.entry_editor.config(bg='SystemButtonFace')
        self.body.msg_box.config(bg='SystemButtonFace')
        self.body.posts_frame.config(bg='SystemButtonFace')
        self.body.msgs_frame.config(bg='SystemButtonFace')
        self.body.entry_frame.config(bg='SystemButtonFace')
        self.body.msg_frame.config(bg='SystemButtonFace')
        self.body.editor_frame.config(bg='SystemButtonFace')


    def update_messages(self):
        '''Creates an event loop that calls to the server for any new inbox messages for the current user'''
        global msgs
        msgs = self.dm.retrieve_new()
        if self._profile_filename == None:
            # Calls the function over again to continue the loop
            self.root.after(5000, self.update_messages)
        else:
            # Creates message objects for the messages that came in from the inbox over the server
            # Adds the messages to the local message logs
            for index, message in enumerate(msgs):
                self._current_profile.add_message(Messages(self.dm.sender, {"from": 'you', "message": msgs[index].message, "timestamp": msgs[index].timestamp}))
            self._current_profile.save_profile(self._profile_filename)

            try:
                # Adds to the tree view the new conversations as they come in from the server
                for index, message in enumerate(self.body.messages):
                    self.body._insert_post_tree(index, message['recipient'])
            except:
                print('')

            try:
                # Updates the msg_box with the messages for the selected recipient/conversation
                self.body.insert_msg_box()
            except Exception as e:
                # Raises the custom exception for if the user does not have any messages on file currently
                # This will allow the program to skip over this step and continue
                raise NoMessages(e)
            finally:
                # Calls the function over again to continue the loop
                self.root.after(5000, self.update_messages)
        
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_settings = tk.Menu(menu_bar)
        # Creates one drop-down menu for file manipulation
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # Creates another drop-down menu for settings
        menu_bar.add_cascade(menu=menu_settings, label='Settings')
        menu_settings.add_command(label='Add User', command=self.add_user)
        menu_settings.add_command(label='Dark Mode On', command=self.dark_mode_on)
        menu_settings.add_command(label='Dark Mode Off', command=self.dark_mode_off)

        # Initializes the Body class
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # Initializes the Footer class
        self.footer = Footer(self.root, send_callback=self.send_msg)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # Sets the size for the DM program
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # Starts up the event loop for the program that will call for any incoming messages
    main.after(5000, app.update_messages)
    # Starts the program
    main.mainloop()