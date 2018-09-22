import requests
from requests.exceptions import RequestException
from urllib.parse import urlencode
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
from hashlib import md5
import re
import os
from multiprocessing import Pool 
from config import *
import pymongo

# 声明MongoDB的数据库对象
client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]


def get_page_index(offset,keyword):
    data={
        'autoload':'true',
        'count':20,
        'cur_tab':3,
        'format':'json',
        'from':'gallery',
        'keyword':keyword,
        'offset':offset
    }

    url = "https://www.toutiao.com/search_content/?" + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 返回请求的内容
            # print(response.text)
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")
        return None

# 解析json数据
def parse_page_index(html):
    data = json.loads(html)
 
    # 判断data数据中data.keys()是否含有键名“data”
    if data and 'data' in data.keys():
           for item in data.get('data'):
                # 构造一个生成器
                yield item.get('article_url')

# 进去详情页爬取数据
def get_page_detail(url):
    try:
        headers = {
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # 返回请求的内容 
            return response.text
        return None
    except RequestException:
        print("请求详情页出错",url)
        return None
# 解析详情页
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    soup.prettify()
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),',re.S)
    result = re.search(images_pattern,html)
    if result:
        result = result.group(1).replace('\\', '')
        data = json.loads(result)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:download_images(image)
            return {
                'title':title,
                'url':url,
                'images':images
            }
#将数据入数据库
def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print("存入MongoDB成功",result)
        return True
    return False 

# 下载图片
def download_images(url):
    print("正在下载",url)
    try:
        headers = {
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            # response.content返回二进制的内容
            save_images(response.content)
        return None
    except RequestException:
        print("请求图片出错",url)
        return None
'''
保存文件到本地
    os.getcwd()当前目录
    md5(content).hexdigest()防止图片重复
'''
def save_images(content):
    file_path ='{0}/{1}.{2}'.format(os.getcwd(),md5(content).hexdigest(),'jpg')
    # 判断文件是否已存在
    if not os.path.exists(file_path) :
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
def main(offset):
    html = get_page_index(offset,KEYWORD)
    # 得到json形式的数据    
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html,url)
            if result :save_to_mongo(result)
            


if __name__ == '__main__':
    groups = [x*20 for x in range(GROUP_START,GROUP_END*1)]
    pool = Pool()
    pool.map(main,groups)
