# James Homer
# jphomer@uci.edu
# 14782048

# Christian Patino
# patinoc1@uci.edu
# 23141678

# extracreditapi.py



import urllib, json
from urllib import request,error
from WebAPI import WebAPI

#API Key: vRZYxUeFLKDrwCvJbZ2Om3GH46cElm1qD7QVsLVt

#Instructions:
#Make a variable and call the Nasa class to receive Nasa's daily article title (no parameters necessary)
#Call your variable.set_apikey(EXTRACREDITAPIKEY)
#Call your variable.load_data()
#Print out your variable.article_title to output the article's title
#Call your variable.transclude(message) to replace all occurrences of '@extracredit' with Nasa's daily article title

EXTRACREDITAPIKEY = "vRZYxUeFLKDrwCvJbZ2Om3GH46cElm1qD7QVsLVt" # replace with the key required for your custom api.

class Nasa(WebAPI):
    key:str = ''
    article_title:str = ''

    def __init__(self) -> None:
        pass


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #Calls the _download_url function that undergoes the API request and receives a response
        url = f"https://api.nasa.gov/planetary/apod?api_key={self.key}"
        r_obj = self._download_url(url)

        #Sets the object's various attributes to the information that is requested from the api server
        if r_obj != None:
            self.article_title = r_obj['title']

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        message = message.replace("@extracredit", self.article_title)
        return message