from urllib.parse import urlparse

from githubData import getGitHubData
from mediumData import getMediumData
from twitterData import getTwitterData


def isThisaPersionFunction(url):
    print(url)
    site = urlparse(url)

    if site.netloc == "github.com" or site.netloc == "www.github.com":
        print("Github")
        getGitHubData(site)
        return False
    if site.netloc == "medium.com" or site.netloc == "www.medium.com":
        print("Medium")
        getMediumData(site)
        return False
    if site.netloc == "twitter.com" or site.netloc == "www.twitter.com":
        print("Twitter")
        getTwitterData(site)
        return False
    print(site)
    return True






#isThisaPersionFunction("https://github.com/mattiashem")
#isThisaPersionFunction("https://medium.com/@pravse")
#isThisaPersionFunction("https://twitter.com/ibuildthecloud")