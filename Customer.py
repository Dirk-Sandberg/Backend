# -*- coding: utf-8 -*-
"""
Created on Wed May 16 20:44:41 2018

@author: Jiaming Fu
"""


class Customer:
    def __init__(self, email, first_name, last_name, billing_address, phone, paypal, username):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.billing_address = billing_address
        self.phone = phone
        self.paypal = paypal
        self.username = username
