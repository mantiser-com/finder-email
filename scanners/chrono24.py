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


def findwatches(brand="rolex"):
    f = open("watches.json", "w")
    page=1
    while page < 40:
        response = ""
        url="https://www.chrono24.com/{0}/index.htm?goal_suggest=1&pageSize=120&showpage={1}".format(brand,page)
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
        watched = soup.find("div", {"class": "result-page-list-schema-json"})
        #print(watched)
        #clean data
        watched = str(watched)
        watched = watched.replace('<div class="result-page-list-schema-json">', '')
        watched = watched.replace('<script type="application/ld+json">', '')
        watched = watched.replace('</script>', '')
        watched = watched.replace('</div>', '')
        try:
            watched_json = json.loads(watched)

            for watch in watched_json['@graph'][1]['offers']:
                     watch['watchid'] =  base64.b64encode(watch['url'].encode('ascii'))
                     watch['watchid'] = watch['watchid'].decode('ascii')
                     watch['timestamp']= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                     watch['type'] = "_watch"
                     watch['tags'] = watch['name'].split()
                     addToNats(watch)
                     print(watch)
                     print("##############")
        except:
            print(watched)
        page = page + 1
        time.sleep(5)
    f.close()


for brand in ['rolex','patekphilippe','audemarspiguet']:
    findwatches(brand)
