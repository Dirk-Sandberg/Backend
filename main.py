# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 08:29:42 2018

@author: Erik
"""

import requests
import json
#import os.path
import SkuParser
import OpponentPicker
#import Voobly
#import VooblyMatchHistory
import EmailSender
import SpreadSheet
import Order
import BillingAddress
import Customer
#import OrderInfoExtracted
import GameSpecificMatchHistory
import SquarespaceApiFunctions as API

SkuParser = SkuParser.SkuParser()
OpponentPicker = OpponentPicker.OpponentPicker()
emailer = EmailSender.Mailer()
SheetWriter = SpreadSheet.SSWriter()

participantFolder = "participantSpreadsheets"
winnersFolder = "winnersSpreadsheets"
miscFolder = "miscellaneousSpreadsheets"
customersSpreadsheet = miscFolder + "/" + "FiveToFightCustomers.csv"
ordersSpreadsheet = miscFolder + "/" + "FiveToFightOrders.csv"

print("Currently, this grabs orders, writes all of them to two databases: FiveToFightCustomers.csv & FiveToFightsOrders.csv\n Enhancements:\n\tRead from database - append new orders\n\tOnly do weekly orders")
# ------------------- Get information about orders from squarespace
beginTime = "2017-05-10T12:00:00Z"
stoppingTime = "2019-05-17T12:30:00Z"
orders = API.getAllOrdersBetween(beginTime, stoppingTime)



# Load in local Customer database
customersDB = []

# Load in local Orders database
availableSKUs = ['FN-DUO', "FN-SOLO", "FN-SQUAD", 'FN-SOLO-01', 'FN-SOLO-02', 'FN-DUO-01', 'FN-DUO-02',
                 'FN-SQUAD-01', 'FN-SQUAD-02', 'AOE-SOLO-01', 'AOE-SOLO-02']  # , 'FN-DUO', 'FN-SQUAD', 'AoE-SOLO']
SKUDictOfLists = {}  # dictionary with keys being the available SKUs. values of the keys are lists
# the lists hold a dict for each player participating in that SKU
for sku in availableSKUs:
    SKUDictOfLists[sku] = []

SKUsThatNeedOpponents = ["AOE-SOLO-01"]  # ["AoE-SOLO-01"]
ordersDB = []

# Read in information from orders on squarespace
print("check if order.line_items['sku'] and username is already recorded in the DB. If so, they signed up twice! breaks things")
for order in orders:
    # Check for any missing fields in the order
    if order['billingAddress']['state'] is None:
        order['billingAddress']['state'] = "N/A"
    if order['billingAddress']['address2'] is None:
        order['billingAddress']['address2'] = ""

    # -------------------- Customer information
    # Init a BillingAddress obj to hold information
    billingAddress = BillingAddress.newBillingAddress(order)

    # Init an Order obj to hold information
    order = Order.newOrder(order, billingAddress.entireBillingAddress)
    # ----- Append to local customer database
    ordersDB.append(order)
    # Init customer obj to hold information
    customer = Customer.newCustomer(order,billingAddress)# get paypal and username from order now, paypal,username)    
    # ------- Append to local customer database
    customersDB.append(customer)


    # --------------------------- Parse SKUs and add everyone in a particular tournament to a list
    for product in order.purchasedProducts:
        sku = product['sku']
        if sku in availableSKUs:
            SKUDictOfLists[sku].append( {
                    'username':  order.username,
                    'email':     order.customer_email,
                    'orderDate': order.created_on,
                    'wins':      0,
                    'opponent':  'N/A',
                    'needsOpponent': 'Yes'
                    })

# ------------------- Write customers database & orders database to file
SheetWriter.writeSheet(customersSpreadsheet, customersDB)
SheetWriter.writeSheet(ordersSpreadsheet, ordersDB)

# --------------------------- Check the tournament list for each product and assign opponents
# Write the participants to a product-specific .csv file
for SKU in availableSKUs:
    if (SKUDictOfLists[SKU]) == []:
        continue # No one signed up for the tournament relating to this SKU. Skip to next SKU
    weeklyTournyFile = participantFolder + "/" + SkuParser.getNextSaturday(order.created_on) + "_" + SKU + "_" + "participants.csv"
    SheetWriter.writeSheet(weeklyTournyFile, SKUDictOfLists[SKU])

nextSat = SkuParser.getNextSaturday(order.created_on)

# Pick opponents for the product-specific .csv file, then send emails
for SKU in SKUsThatNeedOpponents:
    weeklyTournyFile = participantFolder + "/" + SkuParser.getNextSaturday(order.created_on) + "_" + SKU + "_" + "participants.csv"
    OpponentPicker.pickOpponents(weeklyTournyFile)
    print("picked opponents for " + SKU)
    # Send emails for participants in that SKU informing them of their opponent
    playerDict = SheetWriter.readSheet(weeklyTournyFile)
    l= 0
    for player in playerDict:
        if (player['needsOpponent'] == "Yes") and (l == 0):
            mostRecentOpponent = player['opponent'].split(",")[-1]
            l += 1
            emailer.createAndSend('eriksandbergum@gmail.com','Akers','henryboi',SKU,"assignedOpponent", nextSat)
            #emailer.createAndSend(player['email'], player['username'],mostRecentOpponent, SKU, "assignedOpponent", nextSat)



# --------------------- Check who won the AoE games by scraping Voobly

# - Use "Voobly.py" to find user ID number from username

nextSat = SkuParser.getNextSaturday(order.created_on)
prevSat = SkuParser.getPrevSaturday(order.created_on)

# - Use "VooblyMatchHistory.py" to get match history for user ID number
for SKU in SKUsThatNeedOpponents:
    weeklyTournyFile = participantFolder + "/" + SkuParser.getNextSaturday(order.created_on) + "_" + SKU + "_" + "participants.csv"
    playerDict = SheetWriter.readSheet(weeklyTournyFile)
    for player in playerDict:
        player1 = player['username']
        player2 = player['opponent'].split(",")[-1]
        winner = GameSpecificMatchHistory.checkHistory(SKU, player1, player2, prevSat, nextSat)
        # If player won, add a win to their score. This means they get 5$
        #   Player needs a new opponent if they win, unless they are the last player
        if (winner == player1):
            print("GOT HERE")
            player['wins'] = float(player['wins']) + 1
            player['needsOpponent'] = "Yes"
        elif (winner == player2):
            # this player lost
            player['wins'] = float(player['wins']) + 0.0
            player['needsOpponent'] = "No"
        # If there is no winner, they didn't play the game, so refund a portion of their money back
        else:#if (winner == "N/A"):
            player['wins'] = float(player['wins']) + 0.8
            player['needsOpponent'] = "No"
    SheetWriter.writeSheet(weeklyTournyFile, playerDict)

# - Find the opponents name for the user in the text response
# - get the winner of that match, update a table.
# - pick opponents for next round
# - send emails, repeat
# - write winners to giant paypal mass payments sheet
winnersDB = []
print("Probably want to keep better track of transaction IDs")
transactionID = 0
weeklyWinnersFile = winnersFolder + "/" +  "FiveToFightWinners" + nextSat + ".csv"
for sku in availableSKUs:
    dollarsPerWin = 5
    currencyCode = "USD"
    projectTitle = "Five To Fight: " + sku
    transactionID += 1
    weeklyTournyFile = participantFolder + "/" + SkuParser.getNextSaturday(order.created_on) + "_" + sku + "_" + "participants.csv"
    allParticipants = SheetWriter.readSheet(weeklyTournyFile)
    for participant in allParticipants:
        print(sku, participant)
        if participant["wins"] != "0":
            winnersDB.append({"email": participant["email"], "Amount": dollarsPerWin * float(participant["wins"]),
                              "CurrencyCode": currencyCode, "TransactionID": transactionID, "Project": projectTitle})
SheetWriter.writeSheet(weeklyWinnersFile, winnersDB, writeHeader=False)
# format is below
# paypalEmail, amount,currencycode(USD), transactionID, projectTitle
