#
#
#
# File to start
#
# Lissen for events from the que
#!/usr/bin/env python
import asyncio
import os
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import requests
import json
from getemail import getEmails
'''
To test that the search adds data to nats we can use this python file
'''
async def run(loop):
	nc = NATS()
	await nc.connect("{}:4222".format(os.getenv('NATS')), loop=loop)
	async def message_handler(msg):
		subject = msg.subject
		reply = msg.reply
		data = msg.data.decode()
		data_json = json.loads(data)
		print(data_json['url'])
		scan = []
		scan.append(data_json['url'])
		getEmails(scan)
	# Simple publisher and async subscriber via coroutine.
	sid = await nc.subscribe("result", cb=message_handler)





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()