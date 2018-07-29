'''
send emails using python and Gmail API
'''
from __future__ import print_function
from email.mime.text import MIMEText
from email.mime.multipart import  MIMEMultipart
import base64

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/gmail.send'
#CLIENT_SECRET_FILE = 'client_secret.json'
#APPLICATION_NAME = 'Gmail API Python Quickstart'

class Mailer():
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.send'
        self.CLIENT_SECRET_FILE = 'client_secret.json'
        self.APPLICATION_NAME = 'Gmail API Python Quickstart'
        self.credentials = self.get_credentials()
        self.http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=self.http)

    def get_credentials(self):
        """
        Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
    


    def create_message_without_attachment (self, sender, to, subject, message_text_html):
        #Create message container
        message = MIMEMultipart('alternative') # needed for both plain & HTML (the MIME type is multipart/alternative)
        message['Subject'] = subject
        message['From'] = sender
        message['To'] = to
    
        #Create the body of the message (a plain-text and an HTML version)
        #message.attach(MIMEText(message_text_plain, 'plain'))
        message.attach(MIMEText(message_text_html, 'html'))
        
        raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
        raw_message_no_attachment = raw_message_no_attachment.decode()
        body  = {'raw': raw_message_no_attachment}
        return body
    
    def prepareHtmlBody(self,toUsername, opponent, SKU, purpose):
        base = "EmailTemplates/" + SKU + "/" + purpose +"/"
        with open(base + "email_part1.html") as f:
            body = f.read()
        body += toUsername
        with open(base + "email_part2.html") as f:
            body += f.read()
        body += opponent
        with open(base + "email_part3.html") as f:
            body += f.read()
        print ("got body")
        return body
      
    def createAndSend(self,toEmail, toUsername, opponent, SKU, purpose, nextSat):
        htmlMessage = self.prepareHtmlBody(toUsername, opponent, SKU, purpose)
        msg = self.create_message_without_attachment("esandberg@fivetofight.com",toEmail,"Five To Fight Tournament - " + SKU + " - " + nextSat, htmlMessage)
        self.send_message("me",msg)
        
    def send_message(self, user_id, message):
        #def send_message(self,service, user_id, message):
        """Send an email message.
    
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.
    
          Returns:
        Sent Message.
        """
        
        try:
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
        except Exception as error:
            print('An error occurred: %s' % error)
          







