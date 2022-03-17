# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# ds_messenger.py

import ds_protocol
import socket
import time

class DirectMessage:
    '''Helper class for DirectMessenger that is used to create objects that store the recipient, message, and timestamp'''
    message = ''
    def __init__(self, recipient, message, timestamp):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    '''Class that sends and receives messages over a dsuserver'''
    sends = None
    recvs = None
    usr = None

    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.usr = username

        try:
            # Creates a socket connection with the server
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((dsuserver, 3021))
            conn = ds_protocol.init(client)
            # Creates send and receive variables for later use over the server
            self.sends = conn.send
            self.recvs = conn.recv
        except Exception:
            print('Incorrect port or server address.')
            return False

        # Sets up a join message for a user to join the server
        join_msg = '{"join": {"username": "' + username + '","password": "' + password + '", "token":""}}'

        # Sends the message
        ds_protocol.send_msg(join_msg, self.sends)
        resp = self.recvs.readline()
        
        # Parses the message from the server and collects a token
        data_tuple = ds_protocol.extract_json(resp)
        self.token = data_tuple.token

            
    def send(self, message:str, recipient:str) -> bool:
        '''Takes in a message and recipient parameter and sends a message over the dsuserver'''
        # Sets up a dm message for a user to send a message to a recipient over the server
        dm_msg = '{"token":"'+  self.token  +'", "directmessage": {"entry": "' + message + '","recipient": "' + recipient + '","timestamp": ' + str(time.time()) + '}}'

        try:
            # Sends the message
            ds_protocol.send_msg(dm_msg, self.sends)
            json1 = ds_protocol.rec_msg(self.recvs, ' direct message')
            # Converts the contents to a list
            ds_protocol.convert_to_list(json1)
            return True
        except:
            print('Error in sending Direct Message')
            return False

            
    def retrieve_new(self) -> list:
        '''Retrieves all new messages for the user profile from the server'''
        # Sets up an inbox message that is sent to the server to retrieve all new messages
        inbox_msg = '{"token":"'+  self.token  +'", "directmessage": "new"}'

        # Sends the message
        ds_protocol.send_msg(inbox_msg, self.sends)
        resp = ds_protocol.rec_msg(self.recvs, ' new messages')
        # Converts the messages to a list
        msg_list = ds_protocol.convert_to_list(resp)

        try:
            self.sender = resp['response']['messages'][0]['from']
        except:
            print('No messages')

        # Creates and returns a list of DirectMessage objects that contain info from the inbox for later use
        dm_list = []
        for msg in msg_list:
            obj = DirectMessage(self.usr, msg, resp['response']['messages'][0]['timestamp'])
            dm_list.append(obj)
        return dm_list
    
    def retrieve_all(self) -> list:
        '''Retrieves all messages for the user profile from the server'''
        # Sets up an inbox message that is sent to the server to retrieve all messages
        all_msg = '{"token":"' + self.token + '", "directmessage": "all"}'
        # Sends the message
        ds_protocol.send_msg(all_msg, self.sends)
        resp = ds_protocol.rec_msg(self.recvs, ' all messages')
        # Converts the messages to a list
        msg_list = ds_protocol.convert_to_list(resp)

        # Creates and returns a list of DirectMessage objects that contain info from the inbox for later use
        dm_list = []
        for msg in msg_list:
            obj = DirectMessage(self.usr, msg, resp['response']['messages'][0]['timestamp'])
            dm_list.append(obj)
        return dm_list

