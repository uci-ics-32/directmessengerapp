# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

import json
from collections import namedtuple
import socket

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])
Connection = namedtuple('Connection',['socket','send','recv'])

def init(client:socket) -> Connection:
  '''
  The init method should be called for every program that uses the Protocol. The calling program should first establish a 
  connection with a socket object, then pass that open socket to init. init will then create file objects to handle input and output.
  '''
  try:
      f_send = client.makefile('w')
      f_recv = client.makefile('r')
  except:
      print("Invalid socket connection")

  return Connection(
      socket = client,
      send = f_send,
      recv = f_recv
  )


def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    type1 = json_obj['response']['type']
    message= json_obj['response']['message']
    token = json_obj['response']['token']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(type1, message, token)


def send_msg(msg, send):
  '''Sends a message in json format to the server'''
  try:
    send.write(msg + '\r\n')
    send.flush()
  except Exception as e:
    print(e)


def rec_msg(recv, obj):
  '''Receives message from the server and parses it to be readable in string format'''
  resp = recv.readline()
  resp = json.loads(resp)
  if resp["response"]["type"] == 'ok':
    print(f'\nSuccessfully published{obj} to DS Server\n')
  else:
    print(resp['response']['message'] + '\n')

  return resp

def convert_to_list(json):
  '''Extends the message conversion code to account for direct messaging responses'''
  message_list = []

  # Extends message conversion for the response that includes 'message' for the server
  try:
    message = json['response']['message']
    message_list.append(message)
  # Extends message conversion for the response that includes 'messages' for the server
  except:
    messages = json['response']['messages']
    for message in messages:
      message_list.append(message['message'])
  
  return message_list
    

def disconnect(conn):
  '''Closes the send and receive channels'''
  conn.send.close()
  conn.recv.close()
  
if __name__ == '__main__':
  pass
