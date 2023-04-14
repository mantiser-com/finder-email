
import datetime
import os
import json




def addScannerData(type,url,jsonData):
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
        tag = jsonData["data"]["tag"]
    except:
        tag="none"
    try:
        org = jsonData["data"]["org"]
    except:
        org="private"

    scannerData= {
            "url": url,
            "type": type,
            "projectID": projectid,
            "userid": userid,
            "postid": postid,
            "prefix": prefix,
            "dest": dest,
            "scannerid": scannerid,
            "data": jsonData['data'],
            "tag": tag,
            "org": org,
            "timestamp": datetime.datetime.now().isoformat()
        }
    return scannerData