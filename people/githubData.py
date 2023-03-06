import requests
from bs4 import BeautifulSoup
import html5lib
from urllib.parse import urlparse


def getGitHubData(site):
    # Get data from GitHub
    # Path: people/githubData.py
    # Returns: list of dictionaries
    # Example: [{'name': 'John Doe', 'username': 'johndoe', 'email': '
    url = urlparse(site)
    print("Getting GitHub data"+ url.path)
    pathArrayStrin = url.path
    pathArray = pathArrayStrin.split("/")
    path = "https://github.com/"+pathArray[1]
    print(path)
    r = requests.get('http://splash:8050/render.html', params = {'url': path, 'wait' : 2},timeout=10)
    soup=BeautifulSoup(r.content,features="lxml")
    try:
        namediv=soup.find("h1" ,class_="vcard-names")
        name=namediv.find_all('span')[0].getText()
        u_name=namediv.find_all('span')[1].getText()

        company = namediv=soup.find("ul" ,class_="vcard-details")
        companyList=[]
        for i in company:
            companyList.append(i.getText())

        orgsLisy=[]
        orgs = soup.find_all("div" ,class_="border-top color-border-muted pt-3 mt-3 clearfix hide-sm hide-md")
        print(orgs)
        for i in orgs:
            orgsLisy.append(i.getText())

        repos = soup.find("ol" ,class_="d-flex flex-wrap list-style-none gutter-condensed mb-4")
        reposList = repos.find_all("a",class_="pinned-item-meta Link--muted")
        reportHrefs=[]
        for i in reposList:
            reportHrefs.append(i['href'])
        #    orgsLisy.append(i.getText())

        #statstab=soup.find(class_="flex-order-1 flex-md-order-none mt-2 mt-md-0")
        #elements=statstab.find(class_="mb-3")
        #followers=elements.find_all('a')[0].find('span').getText().strip(' ')
        #following=elements.find_all('a')[1].find('span').getText().strip(' ')
        #totstars=elements.find_all('a')[2].find('span').getText().strip(' ')
        #u_img=soup.find(class_="avatar avatar-user width-full border bg-white")['src']
        #repo_num=soup.find(class_="UnderlineNav-body").find('span',class_="Counter").getText()

        dataBack = {
            "name": name,
            "u_name": u_name,
            "company": companyList,
            "repos": reportHrefs,
            "orgs": orgsLisy,
            "source": "github"
        }           
        return dataBack
    except:
        return {"name": "none", "source": "github"}
