from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

try:
    html =  urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
except HTTPError as e:
    print(e)

try:
    bsObj = BeautifulSoup(html)
    nameList = bsObj.findAll("span",{"class":"green"})
# .findAll("span", {"class":{"green", "red"}})
except AttributeError as a:
    print(a)
else:
    for name in nameList:
        print(name.get_text())
# 之前，我们调用 bsObj.tagName 只能获取页面中的第一个指定的标签。
# 现在，我们调用 bsObj.findAll(tagName, tagAttributes) 可以获取页面中所有指定的标签，不再只是第一个了

# .get_text() 会把你正在处理的 HTML 文档中所有的标签都清除，然后返回
# 一个只包含文字的字符串。
# 假如你正在处理一个包含许多超链接、段落和标签的大段源代码，那么 .get_text() 会把这些超链接、段落和标签都清除掉，
# 只剩下一串不带标签的文字。
# 用 BeautifulSoup 对象查找你想要的信息，比直接在 HTML 文本里查找信
# 息要简单得多。通常在你准备打印、存储和操作数据时，应该最后才使
# 用 .get_text()。一般情况下，你应该尽可能地保留 HTML 文档的标签结构