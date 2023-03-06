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
from addNats import addNatsPage
from urllib.parse import urlparse
from people.githubData import getGitHubData
from people.mediumData import getMediumData
from people.twitterData import getTwitterData
from addScannerData import addScannerData


'''
To test that the search adds data to nats we can use this python file
'''


def isThisaPersionFunction(url):
    print(url)
    site = urlparse(url)

    if site.netloc == "github.com" or site.netloc == "www.github.com":
        print("Github")
        return getGitHubData(url)
    elif site.netloc == "medium.com" or site.netloc == "www.medium.com":
        print("Medium")
        return getMediumData(site)
    elif site.netloc == "twitter.com" or site.netloc == "www.twitter.com":
        print("Twitter")
        return getTwitterData(site)
    else:
        print("Not a person")
        return False
    



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
            peopleData = isThisaPersionFunction(data_json['data']['url'])
            

            if peopleData != False:                
                dataToSave= addScannerData("_people",data_json['data']['url'],data_json)
                dataToSave['person']=peopleData
                dataToSave['source']=peopleData['source']
                addNatsPage(dataToSave)
                print("Data sent to nats")

		
    # Simple publisher and async subscriber via coroutine.
	osub = await js.subscribe("result",durable="people")
	data = bytearray()

	while True:
		try:
			msg = await osub.next_msg()
			await message_handler(msg)
			await msg.ack()
		except TimeoutError:
		    pass





if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.run_forever()