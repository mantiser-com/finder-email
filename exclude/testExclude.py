import json
from rediscluster import RedisCluster
import redis
import os
import re
from urllib.parse import urlparse


#rc = RedisCluster(host=os.getenv('REDIS'), port=6379, decode_responses=True)
rc = redis.Redis(host=os.getenv('REDIS'), port=6379, decode_responses=True)

def testExclude(arg,type="url"):
    """Test the arg if we should exclude it or not"""
    sites = rc.lrange("sites",0 ,-1)
    free = rc.lrange("free",0 ,-1)
    maildomain = rc.lrange("maildomain",0 ,-1)
    emails= rc.lrange("emails",0 ,-1)



    
    returnData = True

    if type == "url":
        #cgeck url
        print("check url")
        url = urlparse(arg)
        hostname = str(url.hostname).replace("www.","")
        if hostname in sites:
            print("Match exclude")
            returnData = False

        #Freetext
        for value in free:
            if re.search(value, arg) != None:
                print("Match exclude")
                returnData = False
    
    if type == "email":
        #cgeck email
        print("check email")
        email_first = arg.split("@")[0]
        email_domain = arg.split("@")[1]
        if email_domain in maildomain:
            print("Match exclude on domain")
            returnData = False
        
        for value in free:
            if re.search(value, arg) != None:
                print("Match exclude on free" )
                returnData = False

        if arg in emails:
            print("Match exclude on emails")
            returnData = False

    return returnData

#testExclude("https://www.google.com","url")
#testExclude("matte.hemmingsson@uggla.io","email")
