import asyncio
import nest_asyncio
import datetime
import os
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


async def addNats(loop,to,text):
    nc = NATS()
    await nc.connect("{}:4222".format(os.getenv('NATS')), loop=loop)

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





def addNatsRun(email,url,jsonData):
    to = "upload"
    findData= {
            "email": email,
            "url": url,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    jsonData["results"]= findData
    print("###########- adding to nats")
    #addNats(to,json_upload)
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(addNats(loop,to,jsonData))
    loop.close()
    return {
           "deliverd:upload":"ok" 
    }
