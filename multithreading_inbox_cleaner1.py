#!/usr/bin/python3
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
#multithreaded inbox cleaner
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

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
delete_these_emails = []
inbox_sender_trends = {}
f = open("/home/abprashanth/my_projects/Inbox Cleaner/temp_sender_list.txt","w")



def examine_sender(sender):
	#add the sender to dictionary and increment the frequency
	if(sender in inbox_sender_trends):
		count = inbox_sender_trends[sender]
		count = count+1
		inbox_sender_trends[sender] = count
	else:
		inbox_sender_trends[sender] = 1

def get_spammers_list():
	# we have to read a file and construct a list
	senders_list = open("delete_these_senders.txt","r")
	for line in senders_list:
		#print("==>"+line)
		if(line[0] != "#"):
			delete_these_emails.append(line.strip())
	print("full list --> \n"+str(delete_these_emails))
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
	service = get_service()
	get_email_list(service)
	credentials,http,service = get_service_details()
	

def get_service():
	#get all the credentials
	credentials = get_credentials()
	#use them to make a http request
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	#results = service.users().labels().list(userId='me').execute()
	messages = service.users().messages().list(userId='me').execute()
	return service

def work(message):
	count = 0
	#print(message)
	message = service.users().messages().get(userId='me',id=message).execute()
	headers = message["payload"]["headers"]
	current_id = message["id"]
	for i in headers:
		if(i["name"] == "From"):
			whole_desc = i["value"]
			#get the email in between the < and >
			if("<" in whole_desc):
				sender = whole_desc[whole_desc.index("<")+1 : whole_desc.index(">")]
				print(sender)
				examine_sender(sender)
				count+=1
				if(sender in delete_these_emails):
					print("-", sep=' ', end='', flush=True)
					if((count % 50) == 0):
						print(str(count)+"\n")
					#delete them
					#print("FOUND: "+sender)
					#print("Will delete them soon")
					#service.users().messages().delete(userId = 'me', id=current_id).execute()
				sender_list.append(sender)
			break


def get_email_list(service):
	
	#get a list of all the message IDs
	response = service.users().messages().list(userId='me').execute()
	emails = []
	emails.extend(response["messages"])
	pool = ThreadPool(4)

	#will scan over all the emails in the inbox
	while "nextPageToken" in response:
		response = service.users().messages().list(userId="me", pageToken=response["nextPageToken"]).execute()
		if("messages" in response):
			emails2 = response["messages"]
			emails.extend(emails2)
	
	print("Got all "+str(len(emails))+" emails.")
	f2 = open("/home/abprashanth/my_projects/Inbox Cleaner/temp_message_id.txt","w")
	message_ID_list = []
	for message in emails:
		message_id = message["id"]
		message_ID_list.append(message_id)
	sender_list = []
	f2.write(str(message_ID_list))
	f2.close()

	#make a list of all the senders
	
	pool.map(work,message_ID_list)
	pool.close()
	pool.join()
	#start deleting them
	print("Added them to List Done. OK.")

def dump_to_file(content,filename):
	f = open(filename,"w")
	f.write(str(content))
	f.close()

service = get_service()

if __name__ == "__main__":
	get_spammers_list()
	service = main()
	#dump the trends onto a file
	dump_to_file(inbox_sender_trends,"trends.txt")
	print("Trends written. OK.")