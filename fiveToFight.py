# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 07:39:46 2018
Five To Fight 
Updates database with new user upon registration

@author: Erik
"""

############# Section 1
####### Connect to GMAIL

import imaplib
import email
import pickle
import FiveToFightGmail
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------
gmailName = "FiveToFight.noreply@gmail.com"
gmailPwd = "PaddyWack972134"
gmail = FiveToFightGmail.gmail()    
myServer = imaplib.IMAP4_SSL("imap.gmail.com",993) # Test different port if not working
myServer.login(gmailName,gmailPwd)
status,count = myServer.select('inbox')

# Load Database of orders
with open("FiveToFightOrders.pkl", "rb") as f:
    database = pickle.load(f)
#database = {}
    
# Read new emails and add new orders to database
numEmails = int(count[0].decode())
for i in range(1,1+numEmails):
    emailCounter = str(i).encode()
    status,data = myServer.fetch(emailCounter, '(RFC822)')
    subjectLine, fromLine = gmail.getMeta(data)
    status, data = myServer.fetch(emailCounter, '(UID BODY[TEXT])')
    body = gmail.getBody(data, subjectLine)
    record = gmail.recordData(body, subjectLine)
    try:
        database[record['Order Number']] = record
    except Exception as e:
        pass#print(e)
    myServer.store(emailCounter, '+FLAGS', '\\Deleted') # Message goes to "All Mail"  
myServer.expunge()
myServer.close()
myServer.logout()



# Save Database of Orders
with open("FiveToFightOrders.pkl",'wb') as f:
    pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)
with open("FiveToFightOrder.csv","w") as f:
    keys = list(database.keys())
    header = list(database[keys[0]].keys())
    f.write(",".join(str(x) for x in header) + "\n")
    for key in keys:
        f.write(",".join(str(x) for x in database[key].values()) + "\n")
    
    
    
    
'''
 Send people who made new orders an email on how to play in tournament
'''
