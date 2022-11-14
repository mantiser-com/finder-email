#
#
#
# File to start
#
# Lissen for events from the que
#!/usr/bin/env python
import asyncio
import os
import nats
from nats.errors import TimeoutError
import requests
import json
from singelPage import getPages
'''
To test that the search adds data to nats we can use this python file
'''
async def run(loop):
	nc = await nats.connect(os.getenv('NATS'))
	# Create JetStream context.
	js = nc.jetstream()






	async def message_handler(msg):
		subject = msg.subject
		reply = msg.reply
		data = msg.data.decode()
		print(data)
		data_json = json.loads(json.dumps(eval(data)))
		print(data_json['data']['url'])
		scan = []
		scan.append(data_json['data']['url'])

		# Scan Page
		getPages(scan,data_json)
	# Simple publisher and async subscriber via coroutine.

	osub = await js.subscribe("result",durable="worker")
	data = bytearray()

	while True:
		try:
			msg = await osub.next_msg()
			await message_handler(msg)
			await msg.ack()
		except TimeoutError:
		    print("All data in stream:", len(data))





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()