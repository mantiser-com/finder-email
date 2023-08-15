from urllib.request import urlopen
import json
import uuid
import requests
import pandas as pd
import csv
import time
from flatten_json import flatten


f = open("results.json", "a")
f.write("[")


def arbetsformedlingen(id):
    """
    lets get the if of the add from arbetsformedlingen and extract that data
    """
    with urlopen("https://platsbanken-api.arbetsformedlingen.se/jobs/v1/job/{}".format(id)) as response:
        body = response.read()
    jsonResponse = json.loads(body)
    id_uuid = str(uuid.uuid4()) 
    orgnumber = jsonResponse['company']['organisationNumber']
    company = jsonResponse['company']
    add = flatten(jsonResponse)

    company['uuid'] = id_uuid
    company['work-title'] = jsonResponse['title']
    company['occupation']= jsonResponse['occupation']
    add['uuid'] = id_uuid


    print(company)
    print(add)
    f.write(json.dumps(add)+",\n")


    #https://www.allabolag.se/5568291644
#arbetsformedlingen("s")

def arbetsformedlingensearch(search):
    '''
    Will do a search on arbetsformedlinggen and retunr the pages and sent to the page scraper
    '''
    resp = requests.post(
    'https://platsbanken-api.arbetsformedlingen.se/jobs/v1/search', 
    data=json.dumps({"filters":[{"type":"freetext","value":search}],"order":"relevance","maxRecords":100,"startIndex":0,"toDate":"2023-05-04T19:37:41.350Z","source":"pb"}),
    headers={"Content-Type": "application/json"})

    print(resp)
    searchData = json.loads(resp.text)
    for ad in searchData['ads']:
        arbetsformedlingen(ad['id'])
        #time.sleep(2.4)


def convertJsonToExcel():
    with open('results.json') as json_file:
        jsondata = json.load(json_file)
    
    data_file = open('jsonoutput.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in jsondata:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()


arbetsformedlingensearch("solceller")
f.write("{}")
f.write("]")
f.close()
convertJsonToExcel()
