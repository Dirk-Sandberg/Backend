# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 08:29:42 2018

@author: Erik
"""

import requests
import json
import os.path
import SkuParser
import OpponentPicker
import Voobly
import VooblyMatchHistory
import EmailSender
import SpreadSheet
import Order
import BillingAddress
import Customer
import OrderInfoExtracted

SkuParser = SkuParser.SkuParser()
OpponentPicker = OpponentPicker.OpponentPicker()
emailer = EmailSender.Mailer()
SheetWriter = SpreadSheet.SSWriter()

print(
    "Currently, this grabs all orders ever (at 50+ orders we will need to rework it due to squarespace API), writes all of them to two databases: FiveToFightCustomers.csv & FiveToFightsOrders.csv\n Enhancements:\n\tRead from database - append new orders\n\tOnly do weekly orders\n\tHandle 50+ orders")
# ------------------- Get information about orders from squarespace
beginTime = "2018-05-10T12:00:00Z"
stoppingTime = "2018-05-17T12:30:00Z"
url = "https://api.squarespace.com/1.0/commerce/orders?modifiedAfter=" + beginTime + "&modifiedBefore=" + stoppingTime
header = dict(authorization="Bearer aa96549b-a198-47fe-b260-33a0f3dbf2be")
response = requests.get(url, headers=header)
dictionary = json.loads(response.text)
orders = dictionary['result']

# Load in local Customer database
customersDB = []

# Load in local Orders database
availableSKUs = ['FN-DUO', "FN-SOLO", "FN-SQUAD", "AoE-SOLO", 'FN-SOLO-01', 'FN-SOLO-02', 'FN-DUO-01', 'FN-DUO-02',
                 'FN-SQUAD-01', 'FN-SQUAD-02', 'AOE-SOLO-01', 'AOE-SOLO-02']  # , 'FN-DUO', 'FN-SQUAD', 'AoE-SOLO']
SKUDictOfLists = {}  # dictionary with keys being the available SKUs. values of the keys are lists
# the lists hold a dict for each player participating in that SKU
for sku in availableSKUs:
    SKUDictOfLists[sku] = []  # {"AoE-SOLO-01":[],"AoE-SOLO-02":[]}

SKUsThatNeedOpponents = ["AOE-SOLO-01"]  # ["AoE-SOLO-01"]
ordersDB = []

# Read in information from orders on squarespace

for order in orders:
    # -------------------- Customer information
    # Init a BillingAddress obj to hold information
    billing_address = BillingAddress.BillingAddress(order['billingAddress']['firstName'],
                                                    order['billingAddress']['lastName'],
                                                    order['billingAddress']['address1'],
                                                    order['billingAddress']['address2'],
                                                    order['billingAddress']['city'], order['billingAddress']['state'],
                                                    order['billingAddress']['countryCode'],
                                                    order['billingAddress']['postalCode'],
                                                    order['billingAddress']['phone'])
    # Init a Order obj to hold information
    order = Order.Order(order['customerEmail'], billing_address, order['formSubmission'], order['id'],
                        order['orderNumber'], order['createdOn'], order['subtotal'], order['lineItems'])

    if order.billing_address.state is None:
        order.billing_address.state = "N/A"
    print("Fix this cause of trash avery")
    if order.billing_address.address2 is None:
        order.billing_address.address2 = ""

    products = {}

    # Should we store this into BillingAddress Obj?
    entire_billing_address = billing_address.address1 + ";" + billing_address.address2 + ";" + billing_address.city + ";" + \
                             billing_address.state + ";" + billing_address.country_code + ";" + billing_address.postal_code
    BillingAddress.entire_billing_address = entire_billing_address

    try:
        paypal = order.form_submission[0]['value']
    except:
        paypal = "N/A"
    try:
        username = order.form_submission[1]['value']
    except:
        username = "N/A"

    # Init customer obj to hold information
    customer = Customer.Customer(order.customer_email, order.billing_address.first_name,
                                 order.billing_address.last_name, entire_billing_address,
                                 order.billing_address.phone, paypal, username)

    # ------- Append to local customer database
    customersDB.append(customer)

    # ------------------------- Init OrderInfoExtracted to hold information
    orderInfoExtracted = OrderInfoExtracted.OrderInfoExtracted(order.order_id, order.order_number, order.created_on,
                                                               order.subtotal['value'], order.subtotal['currency'])
    for availableSKU in availableSKUs:
        products[availableSKU] = 0
    for productPurchased in order.line_items:
        products[productPurchased['sku']] += productPurchased['quantity']

    orderInfoExtracted.item_sku = products.keys()

    # ----- Append to local customer database
    ordersDB.append(orderInfoExtracted)

    # --------------------------- Parse SKUs and add everyone in a particular tournament to a list
    for SKU in products:
        if products[SKU] != 0:
            SKUDictOfLists[SKU].append(
                {"username": username, "email": order.customer_email, "orderDate": order.created_on, "wins": 0, "opponent": "N/A",
                 "needsOpponent": "Yes"})

    # for SKU in products:
    #    if products[SKU] != 0:
    #        SkuParser.addPurchasedSkusToTable(SKU,username, email, orderDate)

# ------------------- Write customers database & orders database to file
SheetWriter.writeSheet("FiveToFightCustomers.csv", customersDB)
SheetWriter.writeSheet("FiveToFightOrders.csv", ordersDB)  # only need to call this once now, not in the for loop

# --------------------------- Check the tournament list for each product and assign opponents
# Write the participants to a product-specific .csv file
for SKU in availableSKUs:
    weeklyTournyFile = SkuParser.getNextSaturday(order.created_on) + "_" + SKU + "_" + "participants.csv"
    SheetWriter.writeSheet(weeklyTournyFile, SKUDictOfLists[SKU])

# Pick opponents for the product-specific .csv file
for SKU in SKUsThatNeedOpponents:
    weeklyTournyFile = SkuParser.getNextSaturday(order.created_on) + "_" + SKU + "_" + "participants.csv"
    print("Should change this from orderDate probably!")
    OpponentPicker.pickOpponents(weeklyTournyFile)
    print("picked opponents for " + SKU)

# -------------------
# NEED A WAY TO NOTIFY PLAYERS WHO THEIR OPPONENTS ARE

nextSat = SkuParser.getNextSaturday(order.created_on)

'''
with open("C:\\Users\\Erik\\Desktop\\junk.html", 'r') as file:
    part1 = file.read()
with open("C:\\Users\\Erik\\Desktop\\junk2.html",'r') as file:
    part2 = file.read()
#for i, email in enumerate(emails):
for SKU in SKUsThatNeedOpponents:
    weeklyTournyFile = SkuParser.getNextSaturday(orderDate) + "_" + SKU + "_" + "participants.csv"
    playerDict = SheetWriter.readSheet(weeklyTournyFile)
    for player in playerDict:
        if ( player['needsOpponent'] == "Yes"):
            htmlMessage = "Hi, <b>" + player['username']
            htmlMessage += part1
            htmlMessage += player['opponent'].split(",")[-1]
            htmlMessage += part2
            email = player['email']
            msg = emailer.create_message_without_attachment("esandberg@fivetofight.com",email,"Five To Fight Tournament - " + SKU + " - " + nextSat, htmlMessage)
            emailer.send_message("me",msg)
'''
# ------------------

# --------------------- Check who won the AoE games by scraping Voobly

# - Use "Voobly.py" to find user ID number from username

HistoryChecker = VooblyMatchHistory.VooblyScraper()
nextSat = SkuParser.getNextSaturday(order.created_on)
prevSat = SkuParser.getPrevSaturday(order.created_on)

# - Use "VooblyMatchHistory.py" to get match history for user ID number
for SKU in SKUsThatNeedOpponents:
    weeklyTournyFile = SkuParser.getNextSaturday(order.created_on) + "_" + SKU + "_" + "participants.csv"
    playerDict = SheetWriter.readSheet(weeklyTournyFile)
    for player in playerDict:
        player1 = player['username']
        player2 = player['opponent'].split(",")[-1]
        winner = HistoryChecker.checkHistory(player1, player2, prevSat, nextSat)
        # If player won, add a win to their score. This means they get 5$
        #   Player needs a new opponent if they win, unless they are the last player
        print("\n\nWINNER WAS: " + winner + "\nPLAYER WAS: " + player1 + "\n")
        if (winner == player1):
            print("GOT HERE")
            player['wins'] = float(player['wins']) + 1
            player['needsOpponent'] = "Yes"
        # If there is no winner, they didn't play the game, so refund a portion of their money back
        #   Player should not be assigned a new opponent
        if (winner == player2):
            # this player lost
            player['wins'] = float(player['wins']) + 0.0
            player['needsOpponent'] = "No"
        if (winner == "N/A"):
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
weeklyWinnersFile = "FiveToFightWinners" + nextSat + ".csv"
for sku in availableSKUs:
    dollarsPerWin = 5
    currencyCode = "USD"
    projectTitle = "Five To Fight: " + sku
    transactionID += 1
    weeklyTournyFile = SkuParser.getNextSaturday(order.created_on) + "_" + sku + "_" + "participants.csv"
    allParticipants = SheetWriter.readSheet(weeklyTournyFile)
    for participant in allParticipants:
        print(sku, participant)
        if participant["wins"] != "0":
            winnersDB.append({"email": participant["email"], "Amount": dollarsPerWin * float(participant["wins"]),
                              "CurrencyCode": currencyCode, "TransactionID": transactionID, "Project": projectTitle})
SheetWriter.writeSheet(weeklyWinnersFile, winnersDB, writeHeader=False)
# format is below
# paypalEmail, amount,currencycode(USD), transactionID, projectTitle
