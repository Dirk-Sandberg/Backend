# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:05:18 2018

@author: Jiaming Fu
"""

class Order(): 
    def _init(self, customerEmail, billingAddress, formSubmission, ID, orderNumber, createdOn, subtotal, lineItems ):
        self.customerEmail = customerEmail
        self.billingAddress = billingAddress
        self.formSubmission = formSubmission
        self.ID = ID
        self.orderNumber = orderNumber
        self.createdOn = createdOn
        self.subtotal = subtotal
        self.lineItems = lineItems
        
    
    
