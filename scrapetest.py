from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# html = urlopen("http://pythonscraping.com/pages/page1.html")
# 这行代码主要可能会发生两种异常：
# • 网页在服务器上不存在（或者获取页面的时候出现错误）
#     try:
#         html = urlopen("http://www.pythonscraping.com/pages/page1.html")
#     except HTTPError as e:
#         print(e)
#         # 返回空值，中断程序，或者执行另一个方案
#     else:
#         # 程序继续。注意：如果你已经在上面异常捕捉那一段代码里返回或中断（break），
#         # 那么就不需要使用else语句了，这段代码也不会执行

# # • 服务器不存在
#     if html is None:
#         print("URL is not found")
#     else:
#          # 程序继续

# bsObj = BeautifulSoup(html.read())
# print(bsObj.h1)

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title

title =  getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
        print("Title could not be found")
else:
        print(title)