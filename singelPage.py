# import libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
from addNats import addNatsPage
from getGeoip import  geoipLookup
from pageImage import pageImage




def getPages(site,jsonData):
    #
    # Scrape the site and get all emails
    #
    # process urls one by one until we exhaust the queue
    # getAddedEmails(uid,word)

    # a queue of urls to be crawled
    new_urls = deque(site)
    
    # a set of urls that we have already crawled
    processed_urls = set()


    # a set of crawled emails
    emails = set()
    scanned_page_count=0
    while len(new_urls):
    
        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        scanned_page_count+=1
        if scanned_page_count > 30:
            print("break to man pages scanned")
            break

        processed_urls.add(url)


    
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url
    
        # get url's content
        print("Processing {}".format(url.encode('utf-8')))
        try:
            response = requests.get(url)
        except:
            # ignore pages with errors
            continue
    
        # Lets get some data from the pages we found
        scanPage(url,jsonData)
    
        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text)
    
        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            if "#" in link or "@" in link:
                pass
            else:



                # resolve relative links
                if link.startswith('/'):
                    link = base_url +"/"+ link
                elif not link.startswith('https'):
                    link = path +"/"+ link
                elif not link.startswith('http'):
                    link = path +"/"+ link
                # add the new url to the queue if it was not enqueued nor processed yet
                if not link in new_urls and not link in processed_urls:
                    new_urls.append(link)




def scanPage(url,jsonData):
        # URL setup and HTML request
        urlData = urlparse(url)
        r = requests.get('http://splash:8050/render.html', params = {'url': url, 'wait' : 2})
        soup = BeautifulSoup(r.text, 'html.parser')
        #
        # Setup the basic page data
        #
        title ="none"
        try:
            title = soup.title.text
        except:
            pass

        destination = "_page"

        try:
            destination =jsonData["data"]["destination"]
        except:
            pass


        page ={
            "url":url,
            "userid": jsonData["data"]["userid"],
            "postid": jsonData["data"]["postid"],
            "type": destination,
            "scantime": jsonData["timestamp"],
            "path": urlData.path,
            "hostname": urlData.netloc,
            "params": urlData.params,
            "query": urlData.query,
            "titel" : title,
            "timestamp": "2022-01-13",
            "meta":{},
            "req": jsonData,
            "projectID": "page"
        }
        h1=[]
        h2=[]
        h3=[]

        #
        # Extract info from the page
        #


        for message in soup.find_all("meta"):
            msg_attrs = dict(message.attrs)
            content=""
            property=""
            try:
                content = msg_attrs['content']
            except:
                pass
            try:
                property = msg_attrs['property']
            except:
                pass
            page['meta'][property]=content



        for messageh1 in soup.select("h1"):
            try:
                h1.append(messageh1.text.strip())
            except:
                pass

        for messageh2 in soup.select("h2"):
            try:
                h2.append(messageh2.text.strip())
            except:
                pass

        for messageh3 in soup.select("h3"):
            try:
                h3.append(messageh3.text.strip())
            except:
                pass

        page['h1']=h1
        page['h2']=h2
        page['h3']=h3


        # Adding Geo Data
        geo = geoipLookup(url)
        page['geo']= geo


        #Adding screenshot data
        imageUrl = pageImage(url,jsonData["data"]["postid"])
        page['image']= imageUrl
        #
        # Print the page result
        #
        print(page)
        addNatsPage(page)


