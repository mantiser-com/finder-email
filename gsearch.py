from googlesearch import search
from getemail import getEmails
from sendToFirebase import *
import time
import pprint
from googleapiclient.discovery import build

dontSearch =['youtube','indeed','wikipedia','twitter','bing','yahoo','templatemonster']



#def searchGoogle(words,botid,user,email,mailchimpkey,mailchimplist):
#	'''
#	Search google for this words and get emails fromresult
#	'''
#
#	startScanFirebase(user,botid)
#
#	print("###############################################################################################################")
#	print(words.encode('utf-8'))
#	for url in search(words, stop=50):
#		print(url)
#		serchthis = True
#		for dont in dontSearch:
#			if dont in url:
#				serchthis = False
#			
#		if serchthis:
#			search_url=[url]
#			#try:
#			getEmails(search_url,words,user,botid,mailchimplist,mailchimpkey)
#			print(words.encode('utf8'))
#			#except:
#			#	print("got some error doing next page")
#			
#	print("################################# The End ######################")
#	upload_blob(botid)
#	doneScanFirebase(user,botid)
#

def searchGoogle(words,botid,user):
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyC3Lb6SVMu12srKNQR02ze5S-GLAWbB2Lo")

  res = service.cse().list(
      q=words,
      cx='012631876750147547556:j4ufbjipbdi',
    ).execute()
  for result in res['items']:
	  print(result['formattedUrl'])


