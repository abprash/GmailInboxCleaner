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
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = '/home/abprashanth/my_projects/Inbox Cleaner/client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


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
    #for email in emails:
        
        #get each email's body
        #if the sender is in my list
        #delete the email if the sender is my flagged one
        #else
        #keep iterating
    email1 = emails[0]
    print(str(email1))
    #email1_body = service.users().messages.get(userId = "me", id=email11["id"]).execute()
    #print(email1_body)

def get_email_list():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    messages = service.users().messages().list(userId='me').execute()
    print(len(messages))
    messageId = "15e4a0d8b1cfcdb3"
    message = service.users().messages().get(userId='me',id=messageId).execute();
    #["payload"]["headers"]["from"]
    headers = message["payload"]["headers"]
    for i in headers:
        if(i["name"] == "From"):
            print(i)

    #print(message)
    #print("----->"+str(dir(service.users())))
    labels = results.get('labels', [])
    #print("labels---------"+str(labels))
    response = service.users().messages().list(userId='me').execute()
    emails = []
    emails.extend(response["messages"])

    while "nextPageToken" in response:
        response = service.users().messages().list(userId="me", pageToken=response["nextPageToken"]).execute()
        emails2 = response["messages"]
        emails.extend(emails2)
    #print(email_results)
    print(len(emails))
    
    #lets print one email
    first_email = service.users().messages().get(userId="me", id=emails[0]["id"]).execute()
    print(first_email)
    return emails


if __name__ == '__main__':
    main()