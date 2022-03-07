# James Homer
# jphomer@uci.edu
# 14782048

# lastfm.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.



import urllib, json
from urllib import request,error
from WebAPI import WebAPI


#API Key: e85f8731bd9869562cc8530e60ee1438
#Shared secret: 6347f8724928287cf00bbba9cdd5a3e4

#Instructions:
#Make a variable and call the LastFM class to receive the top track with its artist (no parameters necessary)
#Call set_apikey() to adjust to your api key
#Call your variable.load_data()
#Print out your variable.track to output the top track
#Print out your variable.artist to output the artist of the top track
#Call your variable.transclude(message) to replace all occurrences of '@lastfm' with the top track and its artist

class LastFM(WebAPI):

    key:str = ''
    url:str = ''
    fm_obj:str = ''
    track:str = ''
    artist:str = ''
    

    def __init__(self) -> None:
        pass


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #Calls the _download_url function that undergoes the API request and receives a response
        url = f"https://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={self.key}&format=json"
        r_obj = self._download_url(url)

        #Sets the object's various attributes to the information that is requested from the api server
        if r_obj != None:
            self.fm_obj = r_obj
            self.track = self.fm_obj['tracks']['track'][0]['name']
            self.artist = self.fm_obj['tracks']['track'][0]['artist']['name']
    

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        message = message.replace('@lastfm', self.track + ' by ' + self.artist)
        return message
