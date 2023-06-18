import asyncio
import nest_asyncio
import datetime
import os
import json
import nats
from nats.errors import TimeoutError


async def addNats(loop,to,text):
    nc = await nats.connect("{}".format(os.getenv('NATS')))
    js = nc.jetstream()

    # Stop receiving after 2 messages.
    await js.publish(to, str(text).encode('utf8'))

    # Terminate connection to NATS.
    await nc.close()





def addToNats(jsonData):
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



