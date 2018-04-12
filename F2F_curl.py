# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 08:29:42 2018

@author: Erik
"""

import requests
import json
import skuParser
import os.path
import opponentPicker
import voobly
import VooblyMatchHistory
import EmailSender
import SpreadSheet

SkuParser = skuParser.SkuParser()
OpponentPicker = opponentPicker.OpponentPicker()
emailer = EmailSender.Mailer()
SheetWriter = SpreadSheet.SSWriter()

print("Currently, this grabs all orders ever (at 50+ orders we will need to rework it due to squarespace API), writes all of them to two databases: FiveToFightCustomers.csv & FiveToFightsOrders.csv\n Enhancements:\n\tRead from database - append new orders\n\tOnly do weekly orders\n\tHandle 50+ orders")
# Get information about orders from squarespace
url = "https://api.squarespace.com/1.0/commerce/orders?modifiedAfter=2018-03-15T12:00:00Z&modifiedBefore=2018-04-15T12:30:00Z"
header = dict(authorization= "Bearer aa96549b-a198-47fe-b260-33a0f3dbf2be")
response = requests.get(url, headers = header)
dictionary= json.loads(response.text)
orders = dictionary['result']

# Load in local Customer database
#customersDB = {}
customersDB = []

# Load in local Orders database
availableSKUs = ['FN-DUO', "FN-SOLO", "FN-SQUAD", "AoE-SOLO", 'FN-SOLO-01', 'FN-SOLO-02', 'FN-DUO-01','FN-DUO-02','FN-SQUAD-01','FN-SQUAD-02','AoE-SOLO-01','AoE-SOLO-02']#, 'FN-DUO', 'FN-SQUAD', 'AoE-SOLO']
SKUsThatNeedOpponents = ["AoE-SOLO-01"] #FN-SOLO-01
#ordersDB = {}
ordersDB = []

# Read in information from orders on squarespace

for order in orders:
    # -------------------- Customer information
    products = {}
    email = order['customerEmail']
    firstName = order['billingAddress']['firstName']
    lastName = order['billingAddress']['lastName']
    
    address2 = order['billingAddress']['address2']
    if address2 == None:
        address2 = ""
    billingAddress = order['billingAddress']['address1']+ ";" + address2 + ";" + order['billingAddress']['city'] + ";" + order['billingAddress']['state']+ ";" + order['billingAddress']['countryCode'] + ";" + order['billingAddress']['postalCode']
    
    phone = order['billingAddress']['phone']
    try:
        paypal = order['formSubmission'][0]['value'] 
        foo = order
    except:
        paypal = "N/A"
    try:
        inGameName = order['formSubmission'][1]['value']
    except:
        inGameName = "N/A"
    customersDict = {'email' : email, 'firstName' : firstName, 'lastName' : lastName, 'billingAddress' : billingAddress, 'phone':phone, 'paypal' : paypal, 'inGameName' : inGameName}

    # ------- Append to local customer database
    customersDB.append(customersDict)  
       
        
        
    # ------------------------- Order information
    orderID = order['id']
    orderNumber = order['orderNumber']
    orderDate = order['createdOn']
    subtotal = order['subtotal']['value']
    currency = order['subtotal']['currency']
    for availableSKU in availableSKUs:
        products[availableSKU] = 0
    for productPurchased in order['lineItems']:
        products[productPurchased['sku']] += productPurchased['quantity']

    ordersDict = {'id' : orderID , 'orderNumber' : orderNumber , 'orderDate' : orderDate, 'subtotal' : subtotal, 'currency' : currency}
    for itemSKU in products.keys():
        ordersDict[itemSKU] = products[itemSKU]    
    # ----- Append to local customer database
    ordersDB.append(ordersDict)
   
            
    # --------------------------- Parse SKUs and add everyone in a particular tournament to a list
    for SKU in products:
        if products[SKU] != 0:
            SkuParser.addPurchasedSkusToTable(SKU,inGameName, email, orderDate)
 
# ------------------- Write customers database & orders database to file
SheetWriter.writeSheet("FiveToFightCustomers.csv",customersDB)
SheetWriter.writeSheet("FiveToFightOrders.csv",ordersDB) # only need to call this once now, not in the for loop


# --------------------------- Check the tournament list for each product and assign opponents

for SKU in SKUsThatNeedOpponents:
    print(SKU)
    weeklyTournyFile = SkuParser.getNextSaturday(orderDate) + "_" + SKU + "_" + "participants.csv"
    print("Should change this from orderDate probably!")
    if os.path.isfile(weeklyTournyFile):
        print("exists")
        OpponentPicker.pickOpponents(weeklyTournyFile)
        print("picked opponents for " + SKU)
        
   
     
# -------------------
#NEED A WAY TO NOTIFY PLAYERS WHO THEIR OPPONENTS ARE

nextSat = SkuParser.getNextSaturday(orderDate)
'''
emails = ["HenryDeHockey@gmail.com", "ssandberg11@gmail.com","averyrapson@gmail.com", "eriksandbergum@gmail.com"]
usernames = ["OG_Albino","Tacaro"  , "Elmoooooo", "Alnatheir"]
opponents = ["Alnatheir","Elmooooo","Tacaro"    , "OG_Albino"]
with open("C:\\Users\\Erik\\Desktop\\junk.html", 'r') as file:
    part1 = file.read()
with open("C:\\Users\\Erik\\Desktop\\junk2.html",'r') as file:
    part2 = file.read()
for i, email in enumerate(emails):
    htmlMessage = "Hi, <b>" + usernames[i] + "</b></br></br>"
    htmlMessage += part1
    htmlMessage += opponents[i]
    htmlMessage += part2
    msg = emailer.create_message_without_attachment("esandberg@fivetofight.com",email,"Five To Fight Tournament - " + SKU + " - " + nextSat, htmlMessage)
    emailer.send_message("me",msg)
'''
# ------------------

# --------------------- Check who won the AoE games by scraping Voobly

# - Use "Voobly.py" to find user ID number from username

HistoryChecker = VooblyMatchHistory.VooblyScraper()
nextSat = SkuParser.getNextSaturday(orderDate)
prevSat = SkuParser.getPrevSaturday(orderDate)

# - Use "VooblyMatchHistory.py" to get match history for user ID number
winner = HistoryChecker.checkHistory("Akers","eldemiurgo", prevSat,nextSat)

# - Find the opponents name for the user in the text response
# - get the winner of that match, update a table.
# - pick opponents for next round
# - send emails, repeat
# - write winners to giant paypal mass payments sheet
    # format is below
    # paypalEmail, amount,currencycode(USD), transactionID, projectTitle
    
            
               
    
