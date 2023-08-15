
# import libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import datetime
import time

import base64 
import os



urls = ["https://www.autouncle.se/se/begagnade-bilar?s%5Border_by%5D=cars.created_at+DESC","https://www.autouncle.se/se/begagnade-bilar?page=2&s%5Border_by%5D=cars.created_at+DESC"]

Cars=[]
for url in urls:
    response = requests.get(url, timeout=10)
    print(response)

    soup = BeautifulSoup(response.text,features="lxml")
    for car in soup.find_all("div","listing-item"):
        #print(car)
        carname = car.find("a","listing-item-headline")
        carPrice = car.find("div","listing-item-price")
        carID = carname.attrs['data-car-id']
        #print(carID)
        carLink= car.find("a","listing-item-details-link")
        carCurency = car.find("div",{"data-currency":True})

        carinfo = car.find_all("div","listing-item-info-chip")
        carArray=[]
        for info in carinfo:
            carArray.append(info.text)



        carOb ={
            "name": carname.text,
            "id": carID,
            "link": carLink.attrs['href'],
            "currency": carCurency.attrs['data-currency'],
            "info": carArray,
            "price": carPrice.text
        }
        #print(carOb)
        Cars.append(carOb)
        time.sleep(5)
print(Cars)    
    
