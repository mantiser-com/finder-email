import asyncio
import os
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def addNats(loop,text):
    nc = NATS()
    await nc.connect("{}:4222".format(os.getenv('NATS')))

    # Stop receiving after 2 messages.
    await nc.publish("result", str(text).encode('utf8'))

    # Terminate connection to NATS.
    await nc.close()


def addNatsRunFind():
    json_to_send = {'data':{'action': 'recept', 'url': 'https://www.elino.se/', 'userid': 'test', 'postid':'1','getemail':'2'}}
    loop = asyncio.new_event_loop()
    loop.run_until_complete(addNats(loop,json_to_send))
    loop.close()
    return {
           "deliverd":"ok" 
    }


addNatsRunFind()





