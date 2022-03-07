# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# webapi.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.




from abc import ABC, abstractmethod
import urllib
import json
from urllib import request,error

class WebAPI(ABC):

  key:str = ''

  def _download_url(self, url: str) -> dict:
    '''Takes in a url as a parameter and returns a dictionary (in JSON format)
    that is full of information that is received when a call to an API server is made.
    '''
    response = None
    r_obj = None

    #Attempts to establish a request connection to the provided url and receives a response back in JSON format if it is successful
    try:
        response = urllib.request.urlopen(url)
        json_results = response.read()
        r_obj = json.loads(json_results)
    except urllib.error.HTTPError as e:
        #Error-handling for if the remote API is unavailable
        if e.code == 404 or e.code == 503:
          print('Remote API is unavailable')
          print('Status code: {}'.format(e.code))
          raise e.code
        #Error-handling for if the data is formatted invalidly from the remote API
        elif e.code == 400 or e.code == 401:
          print('Invalid data formatting from the remote API')
          print('Status code: {}'.format(e.code))
          raise e.code
    #Error-handling for if the connection to the Internet is lost
    except urllib.error.URLError as e:
        print('Loss of local connection to the Internet')
        print('Status code: {}'.format(e.reason))
        raise e.reason
    #No matter the result, always closes the response
    finally:
        if response != None:
            response.close()
        
    return r_obj
	
  def set_apikey(self, apikey:str) -> None:
    '''
    Sets the apikey required to make requests to a web API.
    :param apikey: The apikey supplied by the API service
    '''
    self.key = apikey
	
  #abstractmethod ensures that any child classes that inherit this class must include and fill in the abstractmethod functions
  @abstractmethod
  def load_data(self):
    pass
	
  #abstractmethod ensures that any child classes that inherit this class must include and fill in the abstractmethod functions
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass
