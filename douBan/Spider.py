from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql
import json
import demjson
conn = pymysql.connect(host='127.0.0.1', user='root', passwd='123456', db='api', charset='utf8mb4')
cur = conn.cursor()
cur.execute("USE api")
random.seed(datetime.datetime.now())

# 数据库操作
def store(tid, title, content):
    cur.execute('INSERT INTO pages (tid, title, content) VALUES (\"%s\",\"%s\",\"%s\")' % (tid, title, content))
    cur.connection.commit()
    

def getLinks(articleUrl,tag):
    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html)
    links = bsObj.findAll("div",{"class":"main review-item"})
    if tag==1 :
        getTag(links)
        # 总页数
        pages = len(bsObj.find("div",{"class":"paginator"}).findAll("a"))
        if pages > 1:
            pageLinks = bsObj.find("div",{"class":"paginator"}).findAll("a")
            del pageLinks[pages-1]
            for i in range(len(pageLinks)):
                palinks = "https://movie.douban.com"+ pageLinks[i].attrs["href"]
                getLinks(palinks,tag = 2)
                print(1)
    else :
        getTag(links)
        print(3)
# 获取标题和影评
def getContents(Url, tid,title):
    html2 = urlopen(Url).read().decode("UTF8") 
    contentJson = json.loads(html2)
    # 数据处理
    # contentJson["html"] = contentJson["html"].replace("<p>"," ")
    # contentJson["html"] = contentJson["html"].replace("</p>"," ")
    # contentJson["html"] = contentJson["html"].replace("<span>"," ")
    # contentJson["html"] = contentJson["html"].replace("</span>"," ")
    contentJson["html"] = contentJson["html"].replace("\n"," ")
    contentJson["html"] = re.sub("<.*?>","",contentJson["html"])
    # 数据中带有引号等特殊字符时，用于转义
    contentJson["html"] = pymysql.escape_string(contentJson["html"])
    # print(contentJson["html"])
    # 存入数据库
    store(tid, title, contentJson["html"])
    return "success"
def getTag(links):
    for link in links:
        lin = link.attrs["id"]
        title = link.find("img",{"rel":"v:image"}).attrs["title"]
        getContents("https://movie.douban.com/j/review/"+lin+"/full",lin,title)
    return ""

getLinks("https://movie.douban.com/review/best/",tag = 1)



cur.close()
conn.close()

