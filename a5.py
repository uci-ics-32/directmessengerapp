
# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.



from logging import root
from textwrap import fill
import tkinter as tk
from tkinter import BOTH, Toplevel, ttk, filedialog
from turtle import width
from Profile import Post
from NaClProfile import NaClProfile
from ds_client import send

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""
class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # a list of the Post objects available in the active DSU file
        self._posts = [Post]
        
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance 
        self._draw()
    
    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """
    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._posts[index].entry
        self.set_text_entry(entry)
    
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
        #print('current value is %s' % self.entry_editor.get(0, 'end'))
        #deletes all current text in the self.entry_editor widget
        self.entry_editor.delete(0.0, 'end')   # delete between two indices, 0-based
        #inserts the value contained within the text parameter
        self.entry_editor.insert(0.0, text)   # insert new text at a given index
        #print('value is now: ' + self.entry_editor.get())
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_posts(self, posts:list):
        #Populates self._posts with the post data passed in the posts parameter
        self._posts = posts
        #Repopulates the UI with the new post entries
        for index, post in enumerate(self._posts):
            self._insert_post_tree(index, post)
        


    """
    Inserts a single post to the post_tree widget.
    """
    def insert_post(self, post: Post):
        self._posts.append(post)
        id = len(self._posts) - 1 #adjust id for 0-base of treeview widget
        self._insert_post_tree(id, post)


    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """
    def reset_ui(self):
        self.set_text_entry("")
        self.entry_editor.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """
    def _insert_post_tree(self, id, post: Post):
        entry = post.entry
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
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        
        self.entry_editor = tk.Text(editor_frame, width=0)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""
class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """
    def online_click(self):
        #Implements a callback to the chk_button click event
        #Uses the bool of self.is_online.get() to see if the button is clicked
        if self._online_callback is not None:
            self._online_callback(self.is_online.get())

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """
    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """
    def set_status(self, message):
        self.footer_label.configure(text=message)
    
    """
    Call only once upon initialization to add widgets to the frame
    """
    def _draw(self):
        save_button = tk.Button(master=self, text="Save Post", width=20)
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click) 
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

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
        self._is_online = False

        self._profile_filename = None

        self.settings_window = None
        self.settings_entry_edit = None

        self.bio_window = None
        self.bio_entry_edit = None

        self.server_window = None
        self.server_entry_edit = None

        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = NaClProfile()

        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """
    def new_profile(self):
        filename = tk.filedialog.asksaveasfile(filetypes=[('Distributed Social Profile', '*.dsu')])
        self._profile_filename = filename.name

        #Generates keys for a new profile, hardcodes the dsuserver, username, password, and bio, and saves the profile
        self._current_profile.generate_keypair()
        self._current_profile.dsuserver = '168.235.86.101'
        self._current_profile.username = 'vanillamilkshake'
        self._current_profile.password = 'yum'
        self._current_profile.bio = 'bio'
        self._current_profile.save_profile(self._profile_filename)
        self.body.reset_ui()

    
    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """
    def open_profile(self):
        filename = tk.filedialog.askopenfile(filetypes=[('Distributed Social Profile', '*.dsu')])

        #Creates an NaClProfile object and loads the profile and keypair given the file location
        self._profile_filename = filename.name
        self._current_profile = NaClProfile()
        self._current_profile.load_profile(self._profile_filename)
        self._current_profile.import_keypair(self._current_profile.keypair)

        self.body.reset_ui()

        self.body.set_posts(self._current_profile.get_posts())
        #print(self._current_profile.keypair)
    
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def save_profile(self):
        '''Saves the profile'''
        #Creates a new post object that is assigned to what the user types in
        post = Post(self.body.get_text_entry())
        self.body.insert_post(post)

        if self._is_online == True or self._is_online == 1:
            #Sends to the dsuserver
            self.publish(post)

        #Adds the post to the profile and saves it locally
        self._current_profile.add_post(post)
        self._current_profile.save_profile(self._profile_filename)
        #Resets the UI text box
        self.body.set_text_entry("")
 
 
    def publish(self, post:Post):
        '''Calls the send function from the ds_client.py module to send a post and bio to the specified dsuserver'''
        send(self._current_profile.dsuserver, 3021, self._current_profile.username, self._current_profile.password, post.entry, self._current_profile.public_key, self._profile_filename, self._current_profile.bio)


    def save_settings(self):
        '''Saves the username and password and then closes the window'''
        self._save_settings()
        self.settings_window.destroy()
    
    def _save_settings(self):
        '''Saves any changes to the settings'''
        try:
            # Retrieves the username and password from the textbox
            user = self.settings_entry_edit.get(1.0, 2.0).rstrip()
            pw = self.settings_entry_edit.get(2.0, 3.0).rstrip()
            new_user = user[user.index('"') + 1:-1]
            new_pw = pw[pw.index('"') + 1:-1]
            # Per any changes to the username and password, the current profile becomes what the user types in
            # Entries must be between the double quotes
            self._current_profile.username = new_user
            self._current_profile.password = new_pw
            self._current_profile.save_profile(self._profile_filename)
        except:
            print('Username or password error. Make sure input is between double quotes and that a profile is active!')


    def settings(self):
        '''Allows the user to change the username or password for their profile when the 'Settings' menu item is clicked'''
        # Creates a new Toplevel window that will allow for changing of the username and password
        settings = Toplevel()
        self.settings_window = settings
        # Titles the new window
        settings.title("Settings")
        # Sets the size of the new windows
        settings.geometry("360x280")
        settings.minsize(settings.winfo_width(), settings.winfo_height())

        # Creates an entry and editor frame that the user can type in and edit the username and password
        entry_frame = tk.Frame(master=settings, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        # Creates a button widget that saves the new username and password that the user editted
        save_button = tk.Button(master=editor_frame, text="Save Settings", width=20)
        save_button.configure(command=self.save_settings)
        save_button.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        # Creates a text widget that holds the current user's username and password and allows for editting of them
        entry_edit = tk.Text(editor_frame, width=0)
        entry_edit.pack(fill=tk.X, side=tk.TOP, expand=True, padx=5, pady=5)

        # Clears the text box for later use
        entry_edit.delete(0.0, 'end')
        # Inserts the value contained of the current user's username and password
        entry_edit.insert(0.0, f'Username: "{self._current_profile.username}"\nPassword: "{self._current_profile.password}"')

        self.settings_entry_edit = entry_edit

    def save_bio(self):
        '''Saves the bio and then closes the window'''
        self._save_bio()
        self.bio_window.destroy()
    
    def _save_bio(self):
        '''Saves any changes to the bio'''
        try:
            # Retrieves the bio from the textbox
            bio = self.bio_entry_edit.get(1.0, 2.0).rstrip()
            new_bio = bio[bio.index('"') + 1:-1]
            # Per any changes to the bio, the current profile becomes what the user types in
            # Entries must be between the double quotes
            self._current_profile.bio = new_bio
            self._current_profile.save_profile(self._profile_filename)
        except:
            print('Bio entry error. Make sure input is between double quotes and that a profile is active!')


    def bio(self):
        '''Allows the user to change the bio for their profile when the 'Bio' menu item is clicked'''
        # Creates a new Toplevel window that will allow for changing of the bio
        bio = Toplevel()
        self.bio_window = bio
        # Titles the new window
        bio.title("Bio")
        # Sets the size of the new windows
        bio.geometry("360x280")
        bio.minsize(bio.winfo_width(), bio.winfo_height())

        # Creates an entry and editor frame that the user can type in and edit the bio
        entry_frame = tk.Frame(master=bio, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        # Creates a button widget that saves the new bio that the user editted
        save_button = tk.Button(master=editor_frame, text="Save Settings", width=20)
        save_button.configure(command=self.save_bio)
        save_button.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        # Creates a text widget that holds the current user's bio and allows for editting of them
        entry_edit = tk.Text(editor_frame, width=0)
        entry_edit.pack(fill=tk.X, side=tk.TOP, expand=True, padx=5, pady=5)

        # Clears the text box for later use
        entry_edit.delete(0.0, 'end')
        # Inserts the value contained of the current user's bio
        entry_edit.insert(0.0, f'Bio: "{self._current_profile.bio}"')

        self.bio_entry_edit = entry_edit

    def save_server(self):
        '''Saves the server and then closes the window'''
        self._save_server()
        self.server_window.destroy()
    
    def _save_server(self):
        '''Saves any changes to the server'''
        try:
            # Retrieves the server from the textbox
            server = self.server_entry_edit.get(1.0, 2.0).rstrip()
            new_server = server[server.index('"') + 1:-1]
            # Per any changes to the server, the current profile becomes what the user types in
            # Entries must be between the double quotes
            self._current_profile.dsuserver = new_server
            self._current_profile.save_profile(self._profile_filename)
        except:
            print('Server entry error. Make sure input is between double quotes and that a profile is active!')
    
    
    def server(self):
        '''Allows the user to change the server for their profile when the 'Server' menu item is clicked'''
        # Creates a new Toplevel window that will allow for changing of the server
        server = Toplevel()
        self.server_window = server
        # Titles the new window
        server.title("Server")
        # Sets the size of the new windows
        server.geometry("360x280")
        server.minsize(server.winfo_width(), server.winfo_height())

        # Creates an entry and editor frame that the user can type in and edit the server
        entry_frame = tk.Frame(master=server, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        # Creates a button widget that saves the new server that the user editted
        save_button = tk.Button(master=editor_frame, text="Save Settings", width=20)
        save_button.configure(command=self.save_server)
        save_button.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        # Creates a text widget that holds the current user's server and allows for editting of them
        entry_edit = tk.Text(editor_frame, width=0)
        entry_edit.pack(fill=tk.X, side=tk.TOP, expand=True, padx=5, pady=5)

        # Clears the text box for later use
        entry_edit.delete(0.0, 'end')
        # Inserts the value contained of the current user's server
        entry_edit.insert(0.0, f'Server: "{self._current_profile.dsuserver}"')

        self.server_entry_edit = entry_edit


    """
    A callback function for responding to changes to the online chk_button.
    """
    def online_changed(self, value:bool):
        #Changes the _is_online bool according to whether or not the checkbox is clicked
        #If it is clicked, indicates that the post should be sent to the server
        self._is_online = value
        if value == 1:
            self.footer.set_status("Online")
        else:
            self.footer.set_status("Offline")
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # TODO
        menu_file.add_command(label='Settings', command=self.settings)
        # TODO
        menu_file.add_command(label='Bio', command=self.bio)
        # TODO
        menu_file.add_command(label='Server', command=self.server)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # Creates a footer object that now implements a callback to the self.online_changed function
        self.footer = Footer(self.root, save_callback=self.save_profile, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

        #self._online_callback = online_callback

if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Demo")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that modern OSes don't support. 
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize 
    # the class with it.
    MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.mainloop()