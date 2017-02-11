import gmail
import smtplib
import json
from email.mime.text import MIMEText
import os
from twilio.rest import TwilioRestClient
import traceback
from sys import exit

def reading_mail () :  # this function returns a dictionary with email arguments
	g = gmail.Gmail()
	try :
		g.login(os.environ["EMAIL"], os.environ["PASSWORD"])  #logging in to gmail server
	except :
		print ("Unable to authenticate.Got following error :\n{}".format(traceback.format_exc()))
		exit(0)

	unread_mails = g.inbox().mail(unread=True)  #getting all unread mails. It returns all the blank mails
	# total_unread = str(len(unread_mails))
	mail_list = list()
	if len(unread_mails) > 0 :
		for mail in unread_mails :
			mail.fetch()   # getting all the mail attributes like body,subject etc
			# mail_args = {'subject' : mail.subject , 'body' : mail.body , 'sender' : mail.fr}
			msg = "New E-mail !!!\nSender : {}\nSubject : {}".format(mail.fr,mail.subject)
			flag = send_sms(msg)
			if flag :
				mail.read()  #marking the mail as read
		g.logout()  #logging out


def send_sms(message):
	# we import the Twilio client from the dependency we just installed
	try :
		client = TwilioRestClient(os.environ["TWILO_ACCOUNT_SID"] , os.environ["AUTH_TOKEN"])
		client.messages.create(to=os.environ["PHONE_TO"], from_=os.environ["PHONE_FROM"],
		                       body=message)
		return True
	except :
		print ("Following error occured while sending message :\n".format(traceback.format_exc()))
		return False

if __name__ == "__main__" :
	reading_mail()