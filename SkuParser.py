# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 13:10:26 2018

@author: Erik
"""

'''
SKU parser program
Creates a table named "DATE_SKU-Participants" 
    DATE is the date of the upcoming saturday
columns in the table are: 
     ___________________________________________
    | Username |  email  | orderDate | Opponent |
    |----------|---------|-----------|----------|
    
The "Opponent" column is filled in by the OpponentPicker program, which is called by F2F_curl.py
'''

from datetime import datetime, timedelta

class SkuParser():
    def __init__(self):
        self.orders = []
        self.alreadyIn = []
        
    def getNextSaturday(self, orderDate):
        d = datetime.strptime(orderDate[:orderDate.find("T")] , '%Y-%m-%d')
        t = timedelta((12 - d.weekday()) % 7 )
        return (d+t).strftime("%Y-%m-%d")

    def getPrevSaturday(self, orderDate):
        d = datetime.strptime(orderDate[:orderDate.find("T")] , '%Y-%m-%d')
        t = timedelta(( 12 -  d.weekday() ) % 7 - 7 )
        return (d+t).strftime("%Y-%m-%d")
    
    def addPurchasedSkusToTable(self, SKU, username, email, orderDate):
        try:
            with open(self.getNextSaturday(orderDate) + "_" + SKU + "_" + "participants.csv",'r') as file:
                d = file.read().splitlines()
                for participant in d:
                    self.alreadyIn.append(participant.split(",")[0])
        except:
            pass
        with open(self.getNextSaturday(orderDate) + "_" + SKU + "_" + "participants.csv",'a') as file:
            if username not in self.alreadyIn:
                file.write(username +"," + email + "," + orderDate + "," + "No Opponent Yet" + "\n")
        
        
