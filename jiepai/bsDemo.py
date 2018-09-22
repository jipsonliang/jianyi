from bs4 import BeautifulSoup

html="""
<!DOCTYPE html>
<html lang="zh-cmn-Hans" class="ua-windows ua-ff61">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta id="lili" name="renderer" content="webkit" class="test">
    <meta name="referrer" content="always">
    <title>
        豆瓣电影
    </title>
    <meta name="baidu-site-verification" content="cZdR4xxR7RxmM4zE" />
    <meta http-equiv="Pragma" content="no-cache">
    <body>
    <span id="mk">你是？</span>
"""
soup =BeautifulSoup(html)
# .prettify()对代码进行格式化、补全、容错
print(soup.prettify())

# 以字符串形式输出内容
print(soup.title.string)

# 获取属性
print(soup.meta.attrs["http-equiv"])

# 子节点和子孙节点
print(soup.head.contents)

# 父节点和祖先节点
print(soup.meta.parent)
print(list(enumerate(soup.meta.parents)))

'''
标准选择器
find_all()返回所以元素，列表格式
find()返回单个元素
'''
# 根据属性来进行选择 
print(soup.find_all(attrs={"id":"lili"}))
print(soup.find_all(id="lili"))
print(soup.find(class_="test"))

# 根据文本的内容进行选择
print(soup.find_all(text="你是？"))