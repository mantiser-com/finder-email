#
#
#
# File to start
#
# Lissen for events from the que
#!/usr/bin/env python
import pika
import time
from sendToFirebase import doneScanFirebase
from getemail import getEmails
import time
import json
from flask import Flask, request, render_template, url_for, redirect
app = Flask(__name__)

@app.route("/scrape/",methods = ['GET', 'POST'])
def spider():
	if request.method == 'POST':
		#Get payload as text
		payload = request.get_data(as_text=True)
		#Convert paylaod to json
		json_payload = json.loads(payload)

		if json_payload['action']=="scrapeEmail":
			#Starting the weeb scarper for email
		
			getEmails([json_payload['url']],json_payload['id'],json_payload['uid'],json_payload['word'],True)
		elif json_payload['action']=="close":
			#Closing the scanner in firebase
			print("Closying the scanner")
			doneScanFirebase(json_payload['uid'],json_payload['id'])
		else:
			print("Wrong action")


		return "Spider Done !"
	else:
		return "Spinder dont want GET"


@app.route("/")
def home():
	#searchGoogle(mess['words'],mess['botid'],mess['user'],mess['email'],mess['MailChimpList'],mess['userMailChimpKey'])
	#searchGoogle(searchword,botid,userid)
	return "Move in nofing to see here !!"

