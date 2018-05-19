# -*- coding: utf-8 -*-
"""
Created on Wed May 16 21:05:18 2018

@author: Jiaming Fu
"""


class Order:
    def __init__(self, customer_email, billing_address, form_submission, order_id, order_number, created_on, subtotal,
                 line_items):
        self.customer_email = customer_email
        self.billing_address = billing_address
        self.form_submission = form_submission
        self.order_id = order_id
        self.order_number = order_number
        self.created_on = created_on
        self.subtotal = subtotal
        self.line_items = line_items
