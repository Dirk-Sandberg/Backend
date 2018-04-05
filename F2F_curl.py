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


SkuParser = skuParser.SkuParser()
OpponentPicker = opponentPicker.OpponentPicker()

print("Currently, this grabs all orders ever (at 50+ orders we will need to rework it due to squarespace API), writes all of them to two databases: FiveToFightCustomers.csv & FiveToFightsOrders.csv\n Enhancements:\n\tRead from database - append new orders\n\tOnly do weekly orders\n\tHandle 50+ orders")
# Get information about orders from squarespace
url = "https://api.squarespace.com/1.0/commerce/orders?modifiedAfter=2018-03-15T12:00:00Z&modifiedBefore=2018-04-15T12:30:00Z"
header = dict(authorization= "Bearer aa96549b-a198-47fe-b260-33a0f3dbf2be")
response = requests.get(url, headers = header)
dictionary= json.loads(response.text)
orders = dictionary['result']

# Load in local Customer database
customersDB = {}


# Load in local Orders database
availableSKUs = ['FN-DUO', "FN-SOLO", "FN-SQUAD", "AoE-SOLO", 'FN-SOLO-01', 'FN-SOLO-02', 'FN-DUO-01','FN-DUO-02','FN-SQUAD-01','FN-SQUAD-02','AoE-SOLO-01','AoE-SOLO-02']#, 'FN-DUO', 'FN-SQUAD', 'AoE-SOLO']
SKUsThatNeedOpponents = ["AoE-SOLO-01"] #FN-SOLO-01
ordersDB = {}


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
    customersDB[inGameName] = customersDict
      
    # ------- Append to local customer database
    # Currently rewrites the database entirely
    customerUsernames = list(customersDB.keys())
    with open("FiveToFightCustomers.csv","w") as f:
        f.write(",".join( str(x) for x in list(customersDB[customerUsernames[0]].keys())) +"\n")
        for customerUsername in customerUsernames:
            f.write(",".join( str(x) for x in list(customersDB[customerUsername].values())) + "\n")
            
        
        
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
       #if productPurchased['sku'] in products: # Each item in checkout cart is in the productPurchased list
       #    products[productPurchased['sku']] += productPurchased['quantity'] # Record the quantity of each SKU
       #else:
       #    products[productPurchased['sku']] = productPurchased['quantity']
    ordersDict = {'id' : orderID , 'orderNumber' : orderNumber , 'orderDate' : orderDate, 'subtotal' : subtotal, 'currency' : currency}
    for itemSKU in products.keys():
        ordersDict[itemSKU] = products[itemSKU]
    ordersDB[orderID] = ordersDict
    
    # ----- Append to local customer database
    ordersSKUs = list(ordersDB.keys())
    with open("FiveToFightOrders.csv","w") as f:
        f.write(",".join( str(x) for x in list(ordersDB[ordersSKUs[0]].keys())) +"\n")
        for ordersSKU in ordersSKUs:
            f.write(",".join( str(x) for x in list(ordersDB[ordersSKU].values())) + "\n")
            
            
    # --------------------------- Parse SKUs and add everyone in a particular tournament to a list
    for SKU in products:
        if products[SKU] != 0:
            SkuParser.addPurchasedSkusToTable(SKU,inGameName, email, orderDate)
    
# --------------------------- Check the tournament list for each product and assign opponents

for SKU in SKUsThatNeedOpponents:
    print(SKU)
    weeklyTournyFile = SkuParser.getNextSaturday(orderDate) + "_" + SKU + "_" + "participants.csv"
    if os.path.isfile(weeklyTournyFile):
        print("exists")
        OpponentPicker.pickOpponents(weeklyTournyFile)
        print("picked opponents for " + SKU)
        
   
     
# -------------------
'''
NEED A WAY TO NOTIFY PLAYERS WHO THEIR OPPONENTS ARE
'''
# ------------------

# --------------------- Check who won the AoE games by scraping Voobly
# ---- Should probably go into a program named "AoE-Match-Checker.py" or something

# - Use "Voobly.py" to find user ID number from username
vooblyApiKey = "camzdurvkmdaar6cy83iovs6pid3u4gw"
voobly = voobly.Voobly(vooblyApiKey)
voobly.init()
HistoryChecker = VooblyMatchHistory.VooblyScraper()


# - Use "VooblyMatchHistory.py" to get match history for user ID number
# - Find the opponents name for the user in the text response
# - get the winner of that match, update a table.
# - pick opponents for next round
# - send emails, repeat
    
    
            
               
    