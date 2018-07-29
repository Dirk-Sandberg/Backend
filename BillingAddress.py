# -*- coding: utf-8 -*-
"""
Created on Wed May 19 12:06:41 2018

@author: Jiaming Fu
"""


class BillingAddress:
    def __init__(self, first_name, last_name, address1, address2, city, state, country_code, postal_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.country_code = country_code
        self.postal_code = postal_code
        self.phone = phone
        self.entireBillingAddress = self.address1 + ";" + self.address2 + ";" + self.city + ";" + \
                             self.state + ";" + self.country_code + ";" + self.postal_code
   

def newBillingAddress(order):
    newBillingAddress = BillingAddress(order['billingAddress']['firstName'],
        order['billingAddress']['lastName'],
        order['billingAddress']['address1'],
        order['billingAddress']['address2'],
        order['billingAddress']['city'], order['billingAddress']['state'],
        order['billingAddress']['countryCode'],
        order['billingAddress']['postalCode'],
        order['billingAddress']['phone'])
    

    return newBillingAddress
        