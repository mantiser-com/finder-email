import socket
from geolite2 import geolite2
from urllib.parse import urlparse
import redis
import os

rc = redis.Redis(host=os.getenv('REDIS'), port=6379, decode_responses=True)

def geoipLookup(url):
    returnData={}
    parsed_uri = urlparse(url)
    result_url = '{uri.netloc}'.format(uri=parsed_uri)
    print("Check GEO on ip "+result_url)
    ipadd = socket.gethostbyname(result_url)


    #Do we have the geo in redis
    redisIP = rc.get(ipadd)
    print(redisIP)




    reader = geolite2.reader()
    match = reader.get(ipadd)

    try: 
        returnData={
            "url":result_url,
            "city": match['city']['names']['en'],
            "country": match['city']['names']['en'],
            "ip": ipadd,
            "_geo": {"lat":match['location']['latitude'], "lng":match['location']['longitude'] }
        }
        rc.set(ipadd,returnData )
    except:
        returnData={
            "url":result_url,
            "city": "none",
            "country": "none",
            "ip": ipadd
        }

    return returnData


#geoipLookup('www.booli.se')



