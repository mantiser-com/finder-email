import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import datetime
import base64 
import os
import json
from addNats import addToNats
import time
import re

def find(brand="rolex"):
    page=1
    #while page < :
    response = ""

    url="https://www.blocket.se/annonser/hela_sverige/fordon?cg=1000".format(brand,page)
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    #try:
    #    #response = requests.get(url,timeout=10)
    #    response = requests.get(os.getenv('SPLASH'), params = {'url': url, 'wait' : 10, 'timeout' :20},timeout=30)
    #except:
    #       # ignore pages with errors
    #       print("########### Skipping splash error")
    try:
           #response = requests.get(url,timeout=10)
           response = requests.get(url,headers=headers, timeout=10)
    except:
           # ignore pages with errors
           print("########### request error")
            #print(response.text)
    soup = BeautifulSoup(response.text,features="lxml")
    search = soup.find_all("article" )
    for result in search:
        print(result)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(result.find_all("div", {"class": re.compile("styled__Content-sc.*")}))
        #    #text = divs.find_all("div", {"class": "text-block"})
        #    print(divs)
        #    print("##############")
        #pattern = re.compile("styled__Time-.*")
        #a = result.find_all("p", {"class": pattern})
        #print(a)
            
        #clean data



find()
