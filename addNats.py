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
    try:
        projectid = jsonData["data"]["project"]
    except:
        projectid="mantiser"
    try:
        prefix = jsonData["data"]["prefix"]
    except:
        prefix="none"
    try:
        scannerid = jsonData["data"]["scannerid"]
    except:
        scannerid="0000"
    try:
        userid = jsonData["data"]["userid"]
    except:
        userid="0"
    try:
        postid = jsonData["data"]["postid"]
    except:
        postid="0"
    try:
        dest = jsonData["data"]["dest"]
    except:
        dest=[]
    try:
        tech = jsonData["data"]["tech"]
    except:
        tech=[]


    emailData= {
            "email": email,
            "url": url,
            "type": "_email",
            "projectID": projectid,
            "userid": userid,
            "postid": postid,
            "prefix": prefix,
            "dest": dest,
            "tech": tech,
            "scannerid": scannerid,
            "data": jsonData['data'],
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    try:
        emailData['country'] = jsonData["data"]["geo"]["country"]
    except:
        pass
    try:
        emailData['tech'] = jsonData["data"]["tech"]
    except:
        pass
    try:
        emailData['date'] = jsonData["data"]["timestamp"]
    except:
        pass
    try:
        emailData['city'] = jsonData["data"]["gep"]["city"]
    except:
        pass
    try:
        emailData['country'] = jsonData["data"]["gep"]["country"]
    except:
        pass



    print("###########- adding to nats")
    #addNats(to,json_upload)
    print(emailData)
    nest_asyncio.apply()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(addNats(loop,to,emailData))
    loop.close()
    return {
           "deliverd:upload":"ok" 
    }


