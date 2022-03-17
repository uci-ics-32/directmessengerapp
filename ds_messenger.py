import ds_client
import ds_protocol
import socket
import time

class DirectMessage:
    message = ''
    def __init__(self, recipient, message, timestamp):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    sends = None
    recvs = None
    usr = None

    def __init__(self, dsuserver=None, username=None, password=None):
        # TODO: why is token none
        self.token = None
        self.usr = username

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(3)
            client.connect((dsuserver, 3021))
            conn = ds_protocol.init(client)
            self.sends = conn.send
            self.recvs = conn.recv
        except Exception:
            print('Incorrect port or server address.')
            return False


        join_msg = '{"join": {"username": "' + username + '","password": "' + password + '", "token":""}}'

        ds_protocol.send_msg(join_msg, self.sends)
        resp = self.recvs.readline()
        
        # Parses the message from the server and collects a token
        data_tuple = ds_protocol.extract_json(resp)
        self.token = data_tuple.token

            
    def send(self, message:str, recipient:str) -> bool:
        dm_msg = '{"token":"'+  self.token  +'", "directmessage": {"entry": "' + message + '","recipient": "' + recipient + '","timestamp": ' + str(time.time()) + '}}'

        try:
            ds_protocol.send_msg(dm_msg, self.sends)
            json1 = ds_protocol.rec_msg(self.recvs, ' direct message')
            ds_protocol.convert_to_list(json1)
            return True
        except:
            print('Error in sending Direct Message')
            return False

            
    def retrieve_new(self) -> list:
        inbox_msg = '{"token":"'+  self.token  +'", "directmessage": "new"}'

        ds_protocol.send_msg(inbox_msg, self.sends)
        resp = ds_protocol.rec_msg(self.recvs, ' new messages')
        msg_list = ds_protocol.convert_to_list(resp)

        try:
            self.sender = resp['response']['messages'][0]['from']
        except:
            print('No messages')

        dm_list = []
        for msg in msg_list:
            obj = DirectMessage(self.usr, msg, resp['response']['messages'][0]['timestamp'])
            dm_list.append(obj)
        return dm_list
    
    def retrieve_all(self) -> list:
        all_msg = '{"token":"' + self.token + '", "directmessage": "all"}'
        ds_protocol.send_msg(all_msg, self.sends)
        resp = ds_protocol.rec_msg(self.recvs, ' all messages')
        msg_list = ds_protocol.convert_to_list(resp)

        dm_list = []
        for msg in msg_list:
            obj = DirectMessage(self.usr, msg, resp['response']['messages'][0]['timestamp'])
            dm_list.append(obj)
        return dm_list

