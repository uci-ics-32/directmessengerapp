# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# a6.py

# a5.py
# 
# ICS 32 
#
# v0.4
# 
# The following module provides a graphical user interface shell for the DSP journaling program.

from cmath import e
from ctypes import alignment
from pickle import TRUE
import tkinter as tk
from tkinter import E, Toplevel, ttk, filedialog
from turtle import right, width
from Profile import Post
from Profile import Profile
from Profile import Messages
from ds_messenger import DirectMessenger
import time

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
        # self._posts = [Post]
        # self.new = []
        # self.all = []
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
        #REFERENCE

        # self.msg_box.insert(0.0, 'Hello world\n')
        # self.msg_box.tag_configure('tag-right', justify='right')
        # self.msg_box.insert(tk.END, 'Hi there\n', 'tag-right')
        # self.msg_box.insert(tk.END, 'nm wbu?')
        # self.msg_box.configure(state=tk.DISABLED)
        self.insert_msg_box()
    

    def insert_msg_box(self):
        messages = self.messages[index_global]['messages']
        self.msg_box.configure(state=tk.NORMAL)
        self.msg_box.delete(0.0, 'end')
        for message in messages:
            if message['from'] == 'you':
                self.msg_box.insert(tk.END, message['message'] + '\n') 
            else:
                self.msg_box.tag_configure('tag-right', justify='right')
                self.msg_box.insert(tk.END, message['message'] + '\n', 'tag-right')
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
        #print('current value is %s' % self.entry_editor.get(0, 'end'))
        #deletes all current text in the self.entry_editor widget
        self.entry_editor.delete(0.0, 'end')   # delete between two indices, 0-based
        #inserts the value contained within the text parameter
        self.entry_editor.insert(0.0, text)   # insert new text at a given index
        #print('value is now: ' + self.entry_editor.get())
    
    """
    Populates the self._posts attribute with posts from the active DSU file.
    """
    def set_messages(self, messages:list):
        # TODO: Write code to populate self._posts with the post data passed
        # in the posts parameter and repopulate the UI with the new post entries.
        # HINT: You will have to write the delete code yourself, but you can take 
        # advantage of the self.insert_posttree method for updating the posts_tree
        # widget.
        #TODO: Support recipients instead of posts
        self.messages = messages
        #Repopulates the UI with the new post entries
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
        # TODO: reset messages
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
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)

        msgs_frame = tk.Frame(master=self, bg="")
        msgs_frame.pack(fill=tk.BOTH, side=tk.TOP)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP)

        msg_frame = tk.Frame(master=msgs_frame, bg="green")
        msg_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=5)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, pady=5)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        self.msg_box = tk.Text(master=msg_frame, width=0, height=21)
        self.msg_box.configure(state=tk.DISABLED)
        self.msg_box.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=0, pady=0)

        #REFERENCE

        # self.msg_box.insert(0.0, 'Hello world\n')
        # self.msg_box.tag_configure('tag-right', justify='right')
        # self.msg_box.insert(tk.END, 'Hi there\n', 'tag-right')
        # self.msg_box.insert(tk.END, 'nm wbu?')
        # self.msg_box.configure(state=tk.DISABLED)

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
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        # chk_value = self.is_online.get()
        #self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance 
        self._draw()
    
    # """
    # Calls the callback function specified in the online_callback class attribute, if
    # available, when the chk_button widget has been clicked.
    # """
    # def online_click(self):
    #     # TODO: Add code that implements a callback to the chk_button click event.
    #     # The callback should support a single parameter that contains the value
    #     # of the self.is_online widget variable.
    #     pass

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
        send_button = tk.Button(master=self, text="Send", width=20)
        send_button.configure(command=self.save_click)
        send_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        # TODO: change button
        #self.chk_button = tk.Checkbutton(master=self, text="Online", variable=self.is_online)
        #self.chk_button.configure(command=self.online_click) 
        #self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)

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

        self._current_profile = Profile()

        self._current_profile.dsuserver = '168.235.86.101'
        self._current_profile.username = 'vanillamilkshake'
        self._current_profile.password = 'yum'
        self._current_profile.bio = 'mybio'

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
        self._current_profile.load_profile(self._profile_filename)

        self.body.reset_ui()

        self.body.set_messages(self._current_profile.get_messages())
        # TODO: Write code to perform whatever operations are necessary to prepare the UI for
        # an existing DSU file.
        # HINT: You will probably need to do things like load a profile, import encryption keys 
        # and update the UI with posts.
    
    """
    Closes the program when the 'Close' menu item is clicked.
    """
    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """
    def send_msg(self):
        # TODO: Write code to perform whatever operations are necessary to save a 
        # post entry when the user clicks the save_button widget.
        # HINT: You will probably need to do things like create a new Post object,
        # fill it with text, add it to the active profile, save the profile, and
        # clear the editor_entry UI for a new post.
        # This might also be a good place to check if the user has selected the online
        # checkbox and if so send the message to the server.

        # self.body.set_messages(self.body.messages)

        text = self.body.get_text_entry()

        recipient = self.body.messages[index_global]['recipient']

        self.dm.send(text, recipient)

        self._current_profile.add_message(Messages(recipient, {"from": 'me', "message": text, "timestamp": time.time()}))
        #Adds the post to the profile and saves it locally
        self._current_profile.save_profile(self._profile_filename)
        #Resets the UI text box
        self.body.set_text_entry("")

        #self.body.reset_ui()
        self.body.insert_msg_box()


    def save_add(self):
        '''Saves the username and password and then closes the window'''
        self._save_add()
        self.add_window.destroy()
    
    def _save_add(self):
        '''Saves any changes to the settings'''
        try:
            # Retrieves the recipient
            user = self.add_entry_edit.get(1.0, 2.0).rstrip()
            recipient = user[user.index('"') + 1:-1]
            # Entries must be between the double quotes
            self._current_profile.add_message(Messages(recipient))
            #self._current_profile.add_recipient(recipient)
            self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
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
        editor_frame = tk.Frame(master=entry_frame, bg="")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        # Creates a button widget that saves the new user/recipient that the user added
        save_button = tk.Button(master=editor_frame, text="Add User", width=20)
        save_button.configure(command=self.save_add)
        save_button.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        # Creates a text widget that allows for editing of recipient
        entry_edit = tk.Text(editor_frame, width=0)
        entry_edit.pack(fill=tk.X, side=tk.TOP, expand=True, padx=5, pady=5)

        # Clears the text box for later use
        entry_edit.delete(0.0, 'end')
        # Inserts the value contained of the current recipient
        entry_edit.insert(0.0, f'Enter the recipient\'s username: ""')

        self.add_entry_edit = entry_edit


    def update_messages(self):
        global msgs
        msgs = self.dm.retrieve_new()

        # for index, message in enumerate(all):
        #     all_msgs.append(all[index].message)

        # TODO: make the from 'you'
        # TODO: combine it with local file messages
        # TODO: add to msg view according to timestamps

        for index, message in enumerate(msgs):
            # print(message)
            self._current_profile.add_message(Messages(msgs[index].recipient, {"from": 'you', "message": msgs[index].message, "timestamp": msgs[index].timestamp}))

        self._current_profile.save_profile(self._profile_filename)
        
        # {"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript" "timestamp":"1603167689.3928561"}]}}

        # self._current_profile.add_message(Messages(recipient, {"from": 'me', "message": text, "timestamp": time.time()}))
        # self._current_profile.save_profile(self._profile_filename)
        self.body.insert_msg_box()
        self.root.after(5000, self.update_messages)
    
    # """
    # A callback function for responding to changes to the online chk_button.
    # """
    # def online_changed(self, value:bool):
    #     # TODO: 
    #     # 1. Remove the existing code. It has been left here to demonstrate
    #     # how to change the text displayed in the footer_label widget and
    #     # assist you with testing the callback functionality (if the footer_label
    #     # text changes when you click the chk_button widget, your callback is working!).
    #     # 2. Write code to support only sending posts to the DSU server when the online chk_button
    #     # is checked.
    #     if value == 1:
    #         self.footer.set_status("Online")
    #     else:
    #         self.footer.set_status("Offline")
    
    """
    Call only once, upon initialization to add widgets to root frame
    """
    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        menu_bar.add_cascade(menu=menu_settings, label='Settings')
        menu_settings.add_command(label='Add User', command=self.add_user)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar. 

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        
        # HINT: There may already be a class method that serves as a good callback function!
        self.footer = Footer(self.root, send_callback=self.send_msg)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

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
    app = MainApp(main)

    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.after(5000, app.update_messages)
    main.mainloop()