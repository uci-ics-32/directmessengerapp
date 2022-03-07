# James Homer
# jphomer@uci.edu
# 14782048

# openweather.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.



import urllib, json
from urllib import request,error
from datetime import datetime
from WebAPI import WebAPI



#API Key: 63b3bf0aeb696dbac81b065b1f495d0f

class OpenWeather(WebAPI):

    key:str = ''
    zip:str = ''
    ccode:str = ''
    weather_obj:str = ''
    temperature:float = 0
    high_temperature:float = 0
    low_temperature:float = 0
    longitude:float = 0
    latitude:float = 0
    description:str = ''
    humidity:int = 0
    sunset:int = 0
    city:str = ''

    def __init__(self, zipcode='92697', ctrycode='US'):
        self.zip = zipcode
        self.ccode = ctrycode

    
    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #Calls the _download_url function that undergoes the API request and receives a response
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zip},{self.ccode}&appid={self.key}&units=imperial"
        r_obj = self._download_url(url)

        #Sets the object's various attributes to the information that is requested from the api server
        if r_obj != None:
            self.weather_obj = r_obj
            self.temperature = self.weather_obj["main"]["temp"]
            self.high_temperature = self.weather_obj["main"]["temp_max"]
            self.low_temperature = self.weather_obj["main"]["temp_min"]
            self.longitude = self.weather_obj["coord"]["lon"]
            self.latitude = self.weather_obj["coord"]["lat"]
            self.description = self.weather_obj["weather"][0]["description"]
            self.humidity = self.weather_obj["main"]["humidity"]
            self.city = self.weather_obj["name"]
            self.sunset = datetime.fromtimestamp(self.weather_obj["sys"]["sunset"]) 
    

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        message = message.replace("@weather", self.description)
        return message

