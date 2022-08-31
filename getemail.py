import re
import hashlib
import os
import requests
from bs4 import BeautifulSoup
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import json
from firebase_admin import db
from addNats import addNatsRun
from rediscluster import RedisCluster
import redis
import hashlib


emailsHave=[]
#rc = RedisCluster(host=os.getenv('REDIS'), port=6379, decode_responses=True)
rc = redis.Redis(host=os.getenv('REDIS'), port=6379, decode_responses=True)

#Open and load the exclude info
with open('exclude.json') as json_file:
    data = json.load(json_file)

def checkEmail(email,scannerid):
    '''
    This check the email and bot in our redis cache.
    If we already have the email then.

    We hash the bootid and the email and add that to a key 
    '''
    stringToHash =str("{0}-{1}".format(email,scannerid)).encode()
    hashedValues = hashlib.sha224(stringToHash).hexdigest()


    redisScannerId = rc.get(hashedValues)
    if redisScannerId == scannerid:
        print('Already have the email')
        return False
    else:
        rc.set(hashedValues, scannerid)
        #return True



def extractEmail(emails,url,jsonData):
    #Extract the email from the pages
    try:
        scannerid = jsonData["data"]["scannerid"]
    except:
        scannerid="0000"
    for email in emails:

        #Test it we want the email ore not 
        process_email=True
        for skip in data['skipEnds']:
            if email.endswith(skip):
                process_email=False
        if os.getenv('PRIVATE_EMAILS') == True:
            for pattern in data['maildomian']:
                if re.search(pattern, email):
                    print('found a match!')
                    print('Private domain {0}'.format(email))
                    process_email=False

        if checkEmail(email,scannerid):
            process_email=False

        #So lets process the email
        if process_email:
            #Adding email to firebase
            print(email)
            addNatsRun(email,url,jsonData)
            #Adding email ti array so we dont add it again
            emailsHave.append(email)




def getEmails(soap,url,jsonData):
    # extract all email addresses and add them into the resulting set
    print("################# proccess email")
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", soap.text, re.I))
    #emails.update(new_emails)
    extractEmail(new_emails,url,jsonData)
     # create a beutiful soup for the html document
    

    

