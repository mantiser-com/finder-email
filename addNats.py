import asyncio
import nest_asyncio
import datetime
import os
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


async def addNats(loop,to,text):
    nc = NATS()
    await nc.connect("{}:4222".format(os.getenv('NATS')))

    # Stop receiving after 2 messages.
    await nc.publish(to, str(text).encode('utf8'))

    # Terminate connection to NATS.
    await nc.close()


def addNatsRunFind(to,json_upload):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(addNats(loop,to,json_upload))
    loop.close()
    return {
           "deliverd:{0}".format(to):"ok" 
    }



def addNatsPage(jsonData):
    to = "upload"
    jsonData["timestampNats"]= datetime.datetime.now().isoformat()
    print("###########- adding to nats")
    #addNats(to,json_upload)
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(addNats(loop,to,jsonData))
    loop.close()
    return {
           "deliverd:upload":"ok" 
    }





def addNatsRun(email,url,jsonData):
    to = "upload"
    emailData= {
            "email": email,
            "url": url,
            "type": "_email",
             "projectID": "email",
            "userid": jsonData['data']['userid'],
            "postid": jsonData['data']['postid'],
            "scannerid": jsonData['data']['scannerid'],
            "timestamp": datetime.datetime.now().isoformat()
        }
    

    print("###########- adding to nats")
    #addNats(to,json_upload)
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(addNats(loop,to,emailData))
    loop.close()
    return {
           "deliverd:upload":"ok" 
    }
