from urllib.request import build_opener
from urllib.request import HTTPCookieProcessor
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import rethinkdb as r
import json
import re
import time

articles = set() # all article pages we want to crawl

def getLinks(pageUrl):
    global articles
    cj = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cj))
    html = opener.open(pageUrl)
    bsObj = BeautifulSoup(html)
    getData(bsObj)
    time.sleep(5)
    for link in bsObj.findAll("a", href=re.compile("^http://www.nytimes.com/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in articles:
                #We have encountered a new page
                newPage = link.attrs['href']
                print(newPage)
                articles.add(newPage)
                getLinks(newPage)

def getData(bsObj):
    result = []
    storyContentList = bsObj.findAll("p", {"class":"story-body-text story-content"})
    for content in storyContentList:
        result.append(content.get_text())

    titleFull = bsObj.find("meta", {"name":"hdl"})
    if (not titleFull is None):
        title = titleFull.attrs['content']
        print(title)
    else:
        return

    uriFull = bsObj.find("link", {"rel":"canonical"})
    if (not uriFull is None):
        uri = uriFull.attrs['href']
        print(uri)
    else:
        return

    authorFull = bsObj.find("meta", {"name":"byl"})
    if (not authorFull is None):
        author = authorFull.attrs['content']
        print(author)
    else:
        return

    dateFull = bsObj.find("meta", {"name":"pdate"})
    if (not dateFull is None):
        date = dateFull.attrs['content']
        print(date)
    else:
        return

    data = [{
       'title' : title,
       'content' : result,
       'author' : author,
       'uri' : uri,
       'date' : date
    }]
    item = json.dumps(data)
    saveToDB(data)

def saveToDB(item):
    conn = r.connect("localhost", 28015)
    r.db("themis").table("pagesNew2").insert(item).run(conn)

getLinks("http://www.nytimes.com/2016/05/08/fashion/barack-obama-bryan-cranston-table-for-three.html")
