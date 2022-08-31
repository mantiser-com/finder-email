import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from addNats import addNatsPage
from getGeoip import  geoipLookup
import base64 




def pageImage(url,id):
    urlData = urlparse(url)
    baseURL = encoded = base64.b64encode(url.encode('ascii'))
    filename=baseURL.decode('ascii')+"-"+id
    path="/files/"

    r = requests.get('http://splash:8050/render.png', params = {'url': url, 'wait' : 2}, stream=True)
    #print(r.text)
    imgdata = r.raw.read()
    try:
        f = open(path+filename+".png", "wb")
        f.write(imgdata)
        f.close()
        print("Images saved"+filename)
        return filename
    except:
        return "No screenhot"        

