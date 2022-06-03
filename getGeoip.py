import socket
from geolite2 import geolite2
from urllib.parse import urlparse


def geoipLookup(url):
    returnData={}
    parsed_uri = urlparse(url)
    result_url = '{uri.netloc}'.format(uri=parsed_uri)
    print("Check GEO on ip "+result_url)
    ipadd = socket.gethostbyname(result_url)
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
    except:
        returnData={
            "url":result_url,
            "city": "",
            "country": "",
            "ip": ipadd,
            "_geo": {}
        }

    return returnData


#geoipLookup('www.booli.se')



