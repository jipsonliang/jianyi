from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html)
imageLocation = bsObj.find("a", {"id": "logo"}).find("img")["src"]

urlretrieve (imageLocation, "logo.jpg")
# urllib.request.urlretrieve 可以根据文件的 URL 下载文件

# 这段程序从 http://pythonscraping.com 下载 logo 图片，然后在程序运行的文件夹里保存为logo.jpg 文件
