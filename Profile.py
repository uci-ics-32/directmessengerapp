# Profile.py
#
# ICS 32 Winter 2022
# Assignment #2: Journal
#
# Author: Mark S. Baldwin
#
# v0.1.8

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE RIGHT NOW, 
# though can you certainly take a look at it if you are curious.
#
from email import message
import json, time, os
from pathlib import Path

# TODO: finish part 3

"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Post(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently supports two features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    entry property that stores the post message.

    """
    def __init__(self, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)

class Messages(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently supports two features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    entry property that stores the post message.

    """
    # {"recipient": 'mark', "messages": [{"from": 'me', "message": "hi", "timestamp": "1603167689.3928561"}, ]}
    def __init__(self, recipient:str = None, messages:dict = None):
        self._timestamp = 0
        self._recipient = recipient
        self._messages = None
        self.set_recipient(recipient)
        self.set_messages(messages)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        if messages != None:
            dict.__init__(self, recipient=self._recipient, messages=[self._messages])
        else:
            dict.__init__(self, recipient=self._recipient, messages=[])
    
    def set_messages(self, messages):
        if messages != None:
            #print(messages)
            # messages['timestamp'] = time.time()
            self._messages = messages
            dict.__setitem__(self, 'messages', messages)


    def get_messages(self):
        return self._messages

    
    def set_recipient(self, recipient):
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)

        if self._timestamp == 0:
            self._timestamp = time.time()
    

    def get_recipient(self):
        return self._recipient

    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.

    """ 
    # message = property(get_messages, set_messages)
    # recipient = property(get_recipient, set_recipient)
    # timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You will need to 
    use this class to manage the information provided by each new user created within your program for a2. 
    Pay close attention to the properties and functions in this class as you will need to make use of 
    each of them in your program.

    When creating your program you will need to collect user input for the properties exposed by this class. 
    A Profile class should ensure that a username and password are set, but contains no conventions to do so. 
    You should make sure that your code verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = ''            # OPTIONAL
        # self._posts = []         # OPTIONAL
        # self.new = []
        # self.all = []
        self.messages = []

        # {"entry": "Hello World!", "recipient":"ohhimark", "timestamp": "1603167689.3928561"}
        # {"entry": "Hello World!", "recipient":{'name': "ohhimark", {messages:}, "timestamp": "1603167689.3928561"}

        #FINAL:
        # {"recipient": 'mark', "messages": [{"from": 'me', "message": "hi", "timestamp": "1603167689.3928561"}, ]}

    """

    add_post accepts a Post object as parameter and appends it to the posts list. Posts are stored in a 
    list object in the order they are added. So if multiple Posts objects are created, but added to the 
    Profile in a different order, it is possible for the list to not be sorted by the Post.timestamp property. 
    So take caution as to how you implement your add_post code.

    """

    # def add_post(self, post: Post) -> None:
    #     self._posts.append(post)

    def add_message(self, message: Messages):
        # print(message)
        # for key in message.keys():
        #     if key == sender:
        #         message[sender].append(message)
        #     else:
        #         self.recipients.append(message)
        # profile.add_message(Messages('yert', {"from": 'you', "message": "hey", "timestamp": "1603167690.3928561"}))
        # self.messages.append(message)
        # {"recipient": 'mark', "messages": [{"from": 'me', "message": "hi", "timestamp": "1603167689.3928561"}]}
        current_recipients = []
        for input in self.messages:
            current_recipients.append(input['recipient'])
        if message['recipient'] not in current_recipients:
            self.messages.append(message)
        else:
            index1 = 0
            for convo in self.messages:
                if convo['recipient'] == message['recipient']:
                    index1 = self.messages.index(convo)
            self.messages[index1]['messages'].append(message['messages'][0])
            


    """

    del_post removes a Post at a given index and returns True if successful and False if an invalid 
    index was supplied. 

    To determine which post to delete you must implement your own search operation on the posts 
    returned from the get_posts function to find the correct index.

    """

    # def del_post(self, index: int) -> bool:
    #     try:
    #         del self._posts[index]
    #         return True
    #     except IndexError:
    #         return False
        
    """
    
    get_posts returns the list object containing all posts that have been added to the Profile object

    """
    # def get_posts(self) -> list[Post]:
    #     return self._posts

    def get_messages(self):
        #print(self.messages)
        return self.messages

    """

    save_profile accepts an existing dsu file to save the current instance of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str, sender='hi') -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                # for post_obj in obj['_posts']:
                #     post = Post(post_obj[sender], post_obj['timestamp'])
                #     self._posts.append(post)
                #print(obj['messages'])
                for msg_obj in obj['messages']:
                    self.messages.append(msg_obj)
                    # {"recipient": 'mark', "messages": [{"from": 'me', "message": "hi", "timestamp": "1603167689.3928561"}]}

                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()


#Tester code

# profile = Profile()
# profile.add_message(Messages('yert', {"from": 'me', "message": "hi", "timestamp": 0}))
# profile.add_message(Messages('yert', {"from": 'you', "message": "hey", "timestamp": 0}))
# profile.add_message(Messages('yert', {"from": 'you', "message": "fsda", "timestamp": 0}))
# profile.add_message(Messages('hi', {"from": 'me', "message": "yo", "timestamp": 0}))
# profile.add_message(Messages('hi', {"from": 'me', "message": "oi", "timestamp": 0}))
# profile.save_profile('C:\\Users\\James\\Development\\ICS 32 2022\\a6\\ics-32-w22-final-project-30-series-owners\\new.dsu')