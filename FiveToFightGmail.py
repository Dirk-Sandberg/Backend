# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 11:28:06 2018

@author: Erik
"""
import email

class gmail():
    def __init__(self):
        self.working = True
        
    def getMeta(self,emailData):
        for information in emailData:
            if isinstance(information,tuple):
                msg = email.message_from_bytes(information[1])
                # msg.keys()
                subj = msg['subject']
                frm = msg['from']
                return subj, frm
        return None, None
        
    def getBody(self,emailData, subjectLine):
        body = emailData[0][1].decode()
        if ("A New Order has Arrived" in subjectLine):
           startIndex = body.find('Order #')
           endIndex = body[startIndex:].find('blog')
           return body[startIndex : startIndex + endIndex]
        
                 
    def recordData(self,body, subjectLine):
        if ("A New Order has Arrived" in subjectLine):
            
             body = body.split("\r\n")
             if len(body) != 37: # User didn't put in an address line 2, so add an element that is empty for it
                 body = body[:4] + [","] + body[4:]
             for i,x in enumerate(body):
                 print(i,x)
             orderNum = body[0][:body[0].find("(")].replace("Order","").replace("#","").strip()
             date = body[0][body[0].find("(") : body[0].find(")")].replace("(placed on ","").replace(",",";")
             billedName = body[2]
             billedAddress = body[3].replace(",",";") + "; " + body[4].replace(",",";") + "; " + body[5].replace(",",";") + "; " + body[6].replace(",",";")
             card = body[7]
             eMail = body[8]
             phoneNumber = body[9]
             quantity = body[21]
             unitPrice = body[23]
             subtotal = body[25]
             item = body[18]
             ID = body[19]
             itemSubtotal = body[33]
             tax = body[34]
             total = body[35]
             newOrderDict = {'Order Number' : orderNum, 'Date' : date, 'Name' : billedName, 'Billing Address' : billedAddress, 'CC' : card, 
                             'Email' : eMail , 'Phone Number' : phoneNumber, 'Quantity' : quantity, "Item" : item, "Item ID" : ID, "Item Subtotal" : itemSubtotal,
                             "Tax" : tax, "Total" : total}
             return newOrderDict
             
             