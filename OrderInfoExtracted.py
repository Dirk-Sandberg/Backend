# -*- coding: utf-8 -*-
"""
Created on Wed May 16 16:09:18 2018

@author: Jiaming Fu
"""


class OrderInfoExtracted:
    def __init__(self, order_id, order_number, created_on, value, currency):
        self.order_id = order_id
        self.order_number = order_number
        self.created_on = created_on
        self.value = value
        self.currency = currency
        self.item_sku = None
