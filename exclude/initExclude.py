import json
from rediscluster import RedisCluster
import redis
import os


#rc = RedisCluster(host=os.getenv('REDIS'), port=6379, decode_responses=True)
rc = redis.Redis(host=os.getenv('REDIS'), port=6379, decode_responses=True)

def initExclude():
    """Add the defualt list to redis"""
 
    # Opening JSON file
    f = open('exclude/exclude.json')
    data = json.load(f)
    
    #Set the exclude list in redis
    rc.delete("sites")
    rc.lpush("sites", *data['sites'])

    rc.delete("maildomain")
    rc.lpush("maildomain", *data['maildomain'])

    rc.delete("skipEnds")
    rc.lpush("skipEnds", *data['skipEnds'])

    rc.delete("emails")
    rc.lpush("emails", *data['emails'])

    rc.delete("free")
    rc.lpush("free", *data['free'])
    # returns JSON object as 
    # a dictionary

    

    
    # Closing file
    f.close()

    
#initExclude()