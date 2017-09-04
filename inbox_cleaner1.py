#!/usr/bin/python3
from __future__ import print_function
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
#this scope indicates what we can do with the email account
#just read or write access
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
#indicates where the secret file is stored to gain access to the account
#the client secret is read from the 
#'/home/abprashanth/my_projects/Inbox Cleaner/client_secret.json'
CLIENT_SECRET_FILE = ''

APPLICATION_NAME = 'Gmail API Python Inbox Cleaner'
delete_these_emails = ["no-reply@piazza.com","wendy.kan@kaggle.intercom-mail.com",
"jf48@buffalo.edu","donotreply@intel.com","noreply_alerts@velvetjobs.com",
"ellen@startwire.com","monster@email.recjobs.monster.com","jobplanner@startwire.com",
"netsmart@jobs.net","theaerospacecorporation-jobnotification@noreply.jobs2web.com",
"seekerteam@ziprecruiter.com","donotreply@cisco.avature.net"]


def get_credentials():
    """Gets valid user credentials from storage.

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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_service_details():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return credentials,http,service



def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    emails = get_email_list();
    credentials,http,service = get_service_details()
    

def get_email_list():
	#get all the credentials
    credentials = get_credentials()
    #use them to make a http request
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    messages = service.users().messages().list(userId='me').execute()

    #get a list of all the message IDs
    response = service.users().messages().list(userId='me').execute()
    emails = []
    emails.extend(response["messages"])

    while "nextPageToken" in response:
        response = service.users().messages().list(userId="me", pageToken=response["nextPageToken"]).execute()
        emails2 = response["messages"]
        emails.extend(emails2)
    #print(email_results)
    print(len(emails))

    message_ID_list = []
    for message in messages:
    	message_id = message["id"]
    	message_ID_list.append(message_id)
    sender_list = []
    f = open("temp.txt","w")
    #make a list of all the senders
    for message_id in message_ID_list:
    	#messageId = "15e4a0d8b1cfcdb3"
    	message = service.users().messages().get(userId='me',id=message_id).execute()
    	headers = message["payload"]["headers"]
    	for i in headers:
    		if(i["name"] == "From"):
    			sender_list.append(i["value"])
    			break
    f.write(str(sender_list))
    f.close()


if __name__ == "__main__":
	main()