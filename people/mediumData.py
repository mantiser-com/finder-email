import requests
from bs4 import BeautifulSoup
import html5lib


def getMediumData(url):
    print("Getting Medium data "+ url.netloc + url.path)
    dataBack =""
    if (url.path[1] == "@"):
        print("User page")
        dataBack = {
            "name": url.path[1:],
            "source": "medium",
            
            }
    else:
        dataBack = {
            "source": "medium"
            
            }

    return dataBack
