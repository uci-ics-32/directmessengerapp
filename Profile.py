# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# Profile.py
#
# ICS 32 Winter 2022
# Assignment #2: Journal
#
# Author: Mark S. Baldwin
#
# v0.1.8

from email import message
import json, time, os
from pathlib import Path


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


class Messages(dict):
    """ 

    The Messages class is responsible for working with individual user messages. It currently takes in the 
    recipient for a message and a list of dictionaries that act as a message log, each of which
    contain a 'from', 'message', and 'timestamp' attribute

    """
    def __init__(self, recipient:str = None, messages = None):
        self._timestamp = 0
        self._recipient = recipient
        self._messages = None
        self.set_recipient(recipient)
        self.set_messages(messages)
        if messages != None:
            dict.__init__(self, recipient=self._recipient, messages=[self._messages])
        else:
            dict.__init__(self, recipient=self._recipient, messages=[])
    
    def set_messages(self, messages):
        '''Sets the self._messages to the messages passed into the class object'''
        if messages != None:
            self._messages = messages
            dict.__setitem__(self, 'messages', messages)


    def get_messages(self):
        '''Helper function that returns self._messages'''
        return self._messages

    
    def set_recipient(self, recipient):
        '''Sets the recipient to the recipient passed into the class object and updates the dictionary'''
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)

        if self._timestamp == 0:
            self._timestamp = time.time()
    

    def get_recipient(self):
        '''Helper function that returns self._recipient'''
        return self._recipient

    
    def set_time(self, time:float):
        '''Updates the timestamp to the timestamp passed into the class object'''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    

    def get_time(self):
        '''Helper function that returns self._timestamp'''
        return self._timestamp


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
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''            
        self.messages = []



    def add_message(self, message: Messages):
        '''Adds a message to the local file for the profile. If that conversation exists already with that recipient,
        it will instead append the message to the already existing message log. Otherwise, it creates a new message
        container for storing a new conversation'''
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
    
    get_messages returns the list object containing all messages that have been added to the Profile object

    """
    def get_messages(self):
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
                # Stores the messages in a log
                for msg_obj in obj['messages']:
                    self.messages.append(msg_obj)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()