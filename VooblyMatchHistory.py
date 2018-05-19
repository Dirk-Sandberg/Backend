# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:40:30 2018

@author: Erik
"""
apiKey = "camzdurvkmdaar6cy83iovs6pid3u4gw"
apiURL = "http://www.voobly.com/api/validate?key="+apiKey


import requests
import Voobly
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import numpy as np


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
        self.voobly = Voobly.Voobly(self.apiKey)
        self.voobly.init()
        self.connect()
        
    def connect(self):

        firstGetRequest = self.s.get(self.loginUrl)
        postRequest = self.s.post(self.authUrl, data=self.loginInfo)
        
    def checkHistory(self,player,opponent,earliestPossibleDate,LatestPossibleDate):
        print("CHECKING " + player + "\n" )
        #print("scraping data gives UTC time, while web page shows local time.")
        #print("Need to account for that when checking if date is within timeframe")
        vooblyResponse = self.voobly.find_user(player)
        playerIdNumberFromVoobly = vooblyResponse.split("\n")[1].split(",")[0]
        notPassedDate = True # Changes to false if match history is so far back in time it's past the start of the tournament
        pageCounter = 0 # increments based on the match history page number
        pagePart1 = "https://www.voobly.com/profile/view/"+ playerIdNumberFromVoobly + "/Matches/games/matches/user/"+playerIdNumberFromVoobly+"/0/"
        pagePart2 = str(pageCounter) + "#pagebrowser1"
        matchUrl = pagePart1 + pagePart2
        winners = []
        losers = []
        matchDates = []

        while notPassedDate:
            pageHasMatchHistory = False
            getRequest = self.s.get(matchUrl)
            soup = BeautifulSoup(getRequest.content, "html.parser") # parsed html
            #print("SOUPING " + matchUrl)
            #main thing to do: scrape all match history pages until date is outside of range (+1)
            allTDs = soup.findAll("td")
            for i, td in enumerate(allTDs):
                if "have won" in td.text:
                    pageHasMatchHistory = True
                if "has won" in td.text:
                    pageHasMatchHistory = True
                    # Get the winner
                    matchDate = allTDs[i-1].text 
                    winner = td.text
                    loser = allTDs[i+1].text
                    matchDate = self.convertDate(matchDate) # Correct format
                    dateIsInsideMargin = self.checkIfDateIsInsideMargin(matchDate,earliestPossibleDate,LatestPossibleDate)
                    print ("opponent: " + opponent + "\n\tLoser: " + loser + "\n\twinner: " + winner)
                    if ( dateIsInsideMargin == -1 ):
                       # print(matchDate)
                       # print("DATE IS TOO EARLY \n\n")
                        notPassedDate = False
                        break # Stop searching match history by breaking while loop. This date is too far back in time
                    if ( dateIsInsideMargin == 0): # 0 means it IS inside the margin
                        if ( (opponent in loser) or (opponent in winner) ) :
                            if ( not ( ( opponent in winner) and (player in winner) ) ):
                                if ( not ( ( opponent in loser) and (player in loser) ) ):
                                    print(matchDate, winner, loser)
                                    winners.append(winner.replace(" has won",""))
                                    matchDates.append(matchDate)
                                    losers.append(loser)

                           
                            # -- If "OPPONENT" not in loser or winners: they didn't play!                                                                
            if (not pageHasMatchHistory):
                # Stop searching match history by breaking while loop. The player hasn't played any matches earlier than what's displayed on this/the previous page
               # print("PAGE DOESNT HAVE MATCH HISTORY")
                break 
            pageCounter += 1 # Move to next page (i.e. 0/pageCounter#browser1 )            
            pagePart2 = str(pageCounter) + pagePart2[pagePart2.find("#"):] # Replace first character
            matchUrl = pagePart1 + pagePart2

        #print("Need to check to make sure this was the only match they played.")
        #print("Otherwise, need to check all matches and get the first one played  in the timeframe allotted for the match!")

        # match history comes in as most [most recent, ... , last recent]
        # We want the last recent games, so reverse the lists
        winners = winners[::-1]
        losers = losers[::-1]
        matchDates = matchDates[::-1]
        if len(winners) == 0 :
            print("COULDNT FIND ANY WINNERS")
            return "N/A"
        else:
            return winners[0]
        '''
        return winnerOfEarliestMatch
        if (opponent not in winners) and (opponent not in losers):
            return "N/A"
        for i, winner in enumerate(winners):
            if opponent in winner: # If the winner of this match was the selected opponent for this bracket
                # Used "winnner in opponent" rather than winner == opponent because if username is [foo], voobly winner name is 'foo'
                dateIsInsideMargin = self.checkIfDateIsInsideMargin(matchDates[i],earliestPossibleDate,LatestPossibleDate)
                if ( dateIsInsideMargin == 0 ):
                    print("Doesn't check for earliest game played in the interval yet")
                    return opponent
                    #datesAgainstCorrectOpponent.append(datetime.strptime(matchDates[i],"%Y-%m-%d"))#return opponent # opponent was a winner
        
        return player # If no opponent was returned, the player won
        '''
    def close(self):
        self.s.close()
        

    def checkIfDateIsInsideMargin(self,date,left,right):
        # all dates have form yyyy-mm-dd
        left = datetime.strptime(left,  "%Y-%m-%d")
        date = datetime.strptime(date,  "%Y-%m-%d")
        right = datetime.strptime(right,"%Y-%m-%d")
        if (date < left):
            return -1 # Date is too early - use return value to skip the rest of this match
        elif (date > right): # Date is too late - use return value to stop searching web pages
            return 1
        else: # Date is between the start/end date of tournaments.
            return 0

        
    def convertDate(self,date):
        '''
        Converts date format from Voobly (6 March 2018) to standard (yyyy-mm-dd)
        '''
        self.test = date
        print("DATE IS:   " + date)
        if "ago" in date:
            return datetime.today().strftime("%Y-%m-%d")
        if "Today" in date:
            return datetime.today().strftime("%Y-%m-%d")
        if "Yesterday" in date:
            yesterday = datetime.today() - timedelta(1)
            return yesterday.strftime("%Y-%m-%d")        
        else:
            splitDate = date.split(" ")
            months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
            day = splitDate[0]
            month = splitDate[1]
            year = splitDate[2]
            month = months.index(month) + 1
            month = str(month)
            if len(month) != 2:
                month = "0" + month
                if len(day) != 2:
                    day = "0" + day
            return "-".join([year,month,day])
