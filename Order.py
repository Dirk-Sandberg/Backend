# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:05:18 2018

@author: Jiaming Fu
"""


class Order:
    def __init__(self, customer_email, entireBillingAddress, form_submission, order_id, order_number, created_on, subtotal,
                 line_items):
        self.customer_email = customer_email
        self.billingAddress = entireBillingAddress
        self.paypal = "N/A" #form_submission[0] if (form_submission[0] != None) else "N/A"
        self.username = "N/A"
        self.order_id = order_id
        self.order_number = order_number
        self.created_on = created_on
        self.subtotal = subtotal
        # Get the paypal # and username from the custom form we added to the checkout
        try:
            for entryField in form_submission:
                if "paypal" in entryField['label'].lower():
                    self.paypalAccountNumber = entryField['value']
                if "username" in entryField['label'].lower():
                    self.username = entryField['value']
        except TypeError:
            print("Order_ID: " + str(order_id) + " Has no form submission" )
                        
        # Record what products they purchased (the SKUs) and how many of each
        self.purchasedProducts = []
        for purchasedItem in line_items:
            self.purchasedProducts.append({'sku': purchasedItem['sku'], 'quantity': purchasedItem['quantity']})

def newOrder(order, entireBillingAddress):
    newOrder = Order(order['customerEmail'], 
                   entireBillingAddress, 
                   order['formSubmission'], 
                   order['id'],
                   order['orderNumber'], 
                   order['createdOn'], 
                   order['subtotal'], 
                   order['lineItems'])
    return newOrder