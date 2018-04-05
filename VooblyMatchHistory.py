# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:40:30 2018

@author: Erik
"""
apiKey = "camzdurvkmdaar6cy83iovs6pid3u4gw"
apiURL = "http://www.voobly.com/api/validate?key="+apiKey


import requests
import voobly
'''
loginURL = "https://www.voobly.com/login"
authURL = loginURL+"/auth"
matchUrl = "https://www.voobly.com/profile/view/124993231/Matches"

s = requests.session()
loginInfo = {"username":"Akers", "password":"Gr1kjins"}

firstGetRequest = s.get(loginURL) # Get the login page using our session so we save the cookies

postRequest = s.post(authURL,data=loginInfo) # Post data to the login page, the data being my login information

getRequest = s.get(matchUrl) # Get content from a login - restricted page

response = getRequest.content.decode() # Get the actual html text from restricted page

if "Page Access Failed" in response: # True if I'm blocked
    print("Failed")
else:
    print("Worked!") # If I'm not blocked, I have the result I want
'''

class VooblyScraper():
    def __init__(self):
        self.loginUrl = "https://www.voobly.com/login"
        self.authUrl = self.loginUrl + "/auth"
        self.matchUrl = "https://www.voobly.com/profile/view/124993231/Matches"
        self.s = requests.session()
        self.apiKey = "camzdurvkmdaar6cy83iovs6pid3u4gw"
        self.username = "Akers"
        self.password = "Gr1kjins"
        self.loginInfo = {"username":"Akers", "password":"Gr1kjins"}
        print(self.loginInfo)
        self.voobly = voobly.Voobly(self.apiKey)
        self.voobly.init()
        self.connect()
        
    def connect(self):
        firstGetRequest = self.s.get(self.loginUrl)
        postRequest = self.s.post(self.authUrl, data=self.loginInfo)
        
    def checkHistory(self,player,opponent):
        vooblyResponse = self.voobly.find_user(player)
        playerIdNumberFromVoobly = vooblyResponse.split("\n")[1].split(",")[0]
        getRequest = self.s.get("https://www.voobly.com/profile/view/"+ playerIdNumberFromVoobly + "/Matches")
        self.test = getRequest.content.decode()
        
    def close(self):
        self.s.close()
        