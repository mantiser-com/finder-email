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


emailsHave=[]

#Open and load the exclude info
with open('exclude.json') as json_file:
    data = json.load(json_file)




def extractEmail(emails,url):
    #Extract the email from the pages
    for email in emails:

        #Test it we want the email ore not 
        process_email=True
        for skip in data['skipEnds']:
            if email.endswith(skip):
                process_email=False
        if email in emailsHave:
            print('Already have the email')
            process_email=False



        if os.getenv('PRIVATE_EMAILS') == True:
            for pattern in data['maildomian']:
                if re.search(pattern, email):
                    print('found a match!')
                    print('Private domain {0}'.format(email))
                    process_email=False

        #So lets process the email
        if process_email:
            #Adding email to firebase
            print(email)
            addNatsRun(email,url)
            #Adding email ti array so we dont add it again
            emailsHave.append(email)




def getEmails(site):
    #
    # Scrape the site and get all emails
    #
    # process urls one by one until we exhaust the queue
    # getAddedEmails(uid,word)

    # a queue of urls to be crawled
    new_urls = deque(site)
    
    # a set of urls that we have already crawled
    processed_urls = set()


    # a set of crawled emails
    emails = set()
    scanned_page_count=0
    while len(new_urls):
    
        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        scanned_page_count+=1
        if scanned_page_count > 30:
            print("break to man pages scanned")
            break

        processed_urls.add(url)
        #Adding url to firebase
        #addUrlsFirebase(uid,url,word,sid)


    
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
    
        # get url's content
        print("Processing {}".format(url.encode('utf-8')))
        try:
            response = requests.get(url)
        except:
            # ignore pages with errors
            continue
    
        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        #emails.update(new_emails)
        extractEmail(new_emails,url)
    
        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text)
    
        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            if "#" in link or "@" in link:
                pass
            else:



                # resolve relative links
                if link.startswith('/'):
                    link = base_url +"/"+ link
                elif not link.startswith('https'):
                    link = path +"/"+ link
                elif not link.startswith('http'):
                    link = path +"/"+ link
                # add the new url to the queue if it was not enqueued nor processed yet
                if not link in new_urls and not link in processed_urls:
                    new_urls.append(link)
    

