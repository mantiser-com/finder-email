import json
import requests
import os
MUATIC_AUTH= os.getenv('MUATIC_AUTH')
MUATIC_URL= os.getenv('MUATIC_URL')


header={'Authorization': 'Basic {}'.format(MUATIC_AUTH)
        ,'Content-type': 'application/json', 
        'Accept': 'application/json'}



def create_contact_mautic(email,url,jsonData):

    data = {
        'email': email,
        'firstname':'paste',
        'lastname':'hemmingsson',
        'owner':1
        }
    print(jsonData)
    url = '{}/api/contacts/new'.format(MUATIC_URL)
    response = requests.request('POST', url, data=json.dumps(data), headers=header )
    print("Send to mautic")
    print(response.text)
    print(response)


def get_contacts():
    header={'Authorization': 'Basic bWFudGlzZXI6bWFudGlzZXIxMjEy', 'cache-control': "no-cache"}
    url = 'https://mautic.apps.northamlin.com/api/contacts'
    response = requests.request('GET', url, headers=header )
    print(response.text)


#create_contact_mautic("matte@elino.se","mattias","hemmingsson")    
#get_contacts()