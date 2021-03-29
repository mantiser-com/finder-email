import asyncio
import os
import json
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

async def addNats(loop_out,to,text):
    nc = NATS()

    await nc.connect("{}:4222".format(os.getenv('NATS')), loop=loop_out)

    # Stop receiving after 2 messages.
    await nc.publish(to, str(text).encode('utf8'))

    # Terminate connection to NATS.
    await nc.close()


def addNatsRun(to,text):
    loop_out = asyncio.get_event_loop()
    loop_out.create_task(addNats(loop_out,to,text))
    return {
           "deliverd":"ok" 
    }

