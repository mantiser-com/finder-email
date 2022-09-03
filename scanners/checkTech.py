import urllib.request
import sys


header = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"

def wp_check(url):
    wp_domains = []
    isWordpress=False

    url_wpl = url + "/wp-login.php"
    url_wpac = url + "/wp-content/"
    url_wpad = url + "/wp-admin/"
    url_wpc = url + "/wp-cron.php"
    url_wpx = url + "/xmlrpc.php"
    url_wpa = url + "/wp-json/wp/v2/"
    url_wpact = url + "/wp-content/themes/"

    req_wpl = urllib.request.Request(url_wpl, headers={'User-Agent': header})
    req_wpac = urllib.request.Request(url_wpac, headers={'User-Agent': header})
    req_wpact = urllib.request.Request(url_wpact, headers={'User-Agent': header})
    req_wpacp = urllib.request.Request(url_wpact, headers={'User-Agent': header})
    req_wpad = urllib.request.Request(url_wpad, headers={'User-Agent': header})
    req_wpc = urllib.request.Request(url_wpc, headers={'User-Agent': header})
    req_wpx = urllib.request.Request(url_wpx, headers={'User-Agent': header})
    req_wpa = urllib.request.Request(url_wpa, headers={'User-Agent': header})

    print("Check for wordpress")
    try:
        if urllib.request.urlopen(req_wpa):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpl):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpac):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpact):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpacp):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpad):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpc):
            isWordpress=True
    except urllib.error.HTTPError:
        pass
    try:
        if urllib.request.urlopen(req_wpx):
            isWordpress=True
    except urllib.error.HTTPError:
        pass

    return isWordpress

#lets test the site and se what tec we gor in there 
def testPageTech(url,soup):
    wehaveTech=[]
    #Lets start with wordpress
    if wp_check(url):
        wehaveTech.append("wordpress")

    #we have a shopify ?
    print("check for shopify")
    shopify=False
    for message in soup.find_all("meta"):
            msg_attrs = dict(message.attrs)
            try: 
                if msg_attrs['id'] == "shopify-digital-wallet":
                    print("Found shofify")
                    shopify=True
            except:
                pass
            try: 
                if msg_attrs['name'] == "shopify-checkout-api-token":
                    print("Found shofify")
                    shopify=True
            except:
                pass




    if shopify:
        wehaveTech.append('shopify')
    print(wehaveTech)
    return wehaveTech


