# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 11:59:28 2018

Squarespace API Functions

@author: Erik
"""
import requests
import json

def getAllOrdersBetween(startDate, endDate):
    # Use RESTful API to grab the first 50 orders between startDate and endDate
    url = "https://api.squarespace.com/1.0/commerce/orders?modifiedAfter=" + startDate + "&modifiedBefore=" + endDate
    header = dict(authorization="Bearer aa96549b-a198-47fe-b260-33a0f3dbf2be")
    response = requests.get(url, headers=header)
    dictionary = json.loads(response.text)
    orders = dictionary['result']
    
    # If there are more than 50 orders, the squarespace RESTful api returns an indicator to query another page that hold
    # the rest of the orders.
    hasMoreOrders = dictionary['pagination']['hasNextPage']
    while (hasMoreOrders):
        # Use the nextPageCursor field to retrieve the next 50 orders. continue until there are no more orders
        url = "https://api.squarespace.com/1.0/commerce/orders?cursor="+dictionary['pagination']['nextPageCursor']
        response = requests.get(url, headers=header)
        dictionary = json.loads(response.text)
        orders += dictionary['result']
        hasMoreOrders = dictionary['pagination']['hasNextPage']
    return orders

def getAllProductSkus():
   # loginUrl = "https://login.squarespace.com/api/1/login/oauth/provider/authorize?client_id=zsjGTLRojgPsx&redirect_uri=https%3A%2F%2Faccount.squarespace.com%2Fapi%2Faccount%2F1%2Fauth%2Foauth%2Fconnect%3FdestinationUrl%3Dhttps%253A%252F%252Faccount.squarespace.com%252F&state=1%3A1532809926%3Ahqb9k9JTiqp%2FKJOG1Ton4eJDR1E5kq%2Bqr%2BHwiaPN6bU%3D%3AGWAugK40aOpP1fzT%2FsijAZVLuMAmwdaqxFLCJHFt%2B80%3D&options=%7B%22isCloseVisible%22%3Afalse%2C%22isCreateAccountViewActive%22%3Afalse%2C%22thirdPartyAuthenticationMethods%22%3A%5B%22GOOGLE%22%5D%7D#/"
    loginUrl = "https://account.squarespace.com"
    USERNAME = "FiveToFight.noreply@gmail.com"
    PASSWORD = "Gr1kjins"
    form = {'username': USERNAME, 'password': PASSWORD}
    # First need to log in
    with requests.Session() as s:
        # get the cookies
        firstGetRequest = s.get(loginUrl)
        r = s.post("/api/1/login/oauth/provider/authorize/user/re-auth", data=form)#/oauth/provider/authorize", data=form)
        print(r)
        print(r.text)
        # After log in, can retrieve all products
        url = "https://fivetofight.com/api/1/commerce/products"
        apiKey1 = "Bearer 5b12e25e-7d92-41d8-8622-734f6aafe9b8"
        apiKey2 = "Bearer Aa96549b-a198-47fe-b260-33a0f3dbf2be"
        header = dict(authorization=apiKey1)
        response = s.get(url, headers=header)
        dictionary = json.loads(response.text)
    