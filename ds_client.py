# James Homer
# jphomer@uci.edu
# 14782048

# ds_client.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

import socket
import ds_protocol
import time


def has_whitespace(string):
  '''Checks if a given string has whitespace'''
  if len(string.strip()) == 0:
    return True
  return False

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  if type(server) != str or type(port) != int or type(username) != str or type(password) != str or type(message) != str or type(bio) != (None or str):
    print('Invalid type(s) used.')
    return False

  # Establishes connection to the server
  try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3)
    client.connect((server, port))
    conn = ds_protocol.init(client)
    send = conn.send
    recv = conn.recv
  except Exception as e:
    print('Incorrect port or server address.')
    return False


  def join():
    '''Attempts to connect to a server'''
    join_msg = '{"join": {"username": "' + username + '","password": "' + password + '", "token":""}}'

    ds_protocol.send_msg(join_msg, send)
    resp = recv.readline()
    
    # Parses the message from the server and collects a token
    try:
      data_tuple = ds_protocol.extract_json(resp)
      token = data_tuple.token
      return token
    except Exception:
      print('Invalid password or username already taken')
      return False

  def post(token):
    '''Attempts to post a message to the server that was joined through join()'''
    timestamp = str(time.time())

    # Message to be sent to the server
    post_msg = '{"token":"'+  token  +'", "post": {"entry": "'+ message +'","timestamp": "'+ timestamp +'"}}'

    if has_whitespace(message):
      print('Error. Post cannot be whitespace')
      return False
    else:
      ds_protocol.send_msg(post_msg, send)
      ds_protocol.rec_msg(recv, 'post')
    return True
    


  def biography(token, bio):
    '''Attempts to post a new biography or biography change to the server'''
    bio_msg = '{"token":"'+  token  +'", "bio": {"entry": "'+ bio +'","timestamp": ""}}'

    if has_whitespace(bio):
      print('Error. Bio cannot have whitespace')
      return False
    else:
      ds_protocol.send_msg(bio_msg, send)
      ds_protocol.rec_msg(recv, 'bio')
    return True


  token = join() 

  # If anything fails, False is returned to indicate an error with the program
  if token == False:
    return False
  elif post(token) == False:
    return False
  elif biography(token, bio) == False:
    return False
  
  ds_protocol.disconnect(conn)

  # Returns true if everything works as intended
  return True
