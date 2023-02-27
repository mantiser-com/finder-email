import requests
from bs4 import BeautifulSoup
import html5lib


def getTwitterData(url):
    print("Getting twitter data "+ url.netloc + url.path)
    if (url.path[0] == "/" and url.netloc == "twitter.com"):
        print("User page")
        dataBack = {
            "name": url.path,
            "source": "twitter",
            
            }           
    return dataBack