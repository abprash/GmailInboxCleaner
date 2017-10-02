#split the text based on commas
#sample entry - 'info@twitter.com': 95, 
#then further split on :
#then store LHS and RHS

path = "/home/abprashanth/my_projects/Inbox Cleaner/InboxCleaner/trends.txt"
f1 = open(path,"r")
contents = f1.read()
#remove the first and last { and }
contents = contents[1:len(contents)-1]
split_contents = contents.split(",")
#print(str(type(split_contents)))
#split contents is a list
to_write = open("/home/abprashanth/my_projects/Inbox Cleaner/InboxCleaner/parsed_mails.txt","w")
for item in split_contents:
	email_count = item.split(":")
	#email_count = email_count[0].strip()
	email = email_count[0]
	count = email_count[1]
	to_write.write(str(email+"-"+count+"\n"))
to_write.close()
f1.close()
