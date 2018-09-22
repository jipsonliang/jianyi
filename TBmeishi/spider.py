from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
from config  import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

options = webdriver.FirefoxOptions()
#options.set_headless(True)
options.add_argument("--headless") #设置火狐为headless无界面模式
options.add_argument("--disable-gpu")
browser = webdriver.Firefox(firefox_options=options)
wait = WebDriverWait(browser,10)
def search():
    try:
        browser.get('https://www.taobao.com/')
        # 设置等待，直到所需要的元素加载完成
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,".btn-search"))
        )
        input.send_keys('美食')
        submit.click()
        # 等待翻页元素加载完
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.total'))
        )
        get_products()
        return total.text
    except TimeoutException:
        # 重新请求
        return search()
def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,"input.input:nth-child(2)"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,"span.btn:nth-child(4)"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        # 判断所选元素中的值是否于要对比的值相等
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR,'li.active > span:nth-child(1)'),str(page_number))
        )
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item'))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败',result)
def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    # 从第二页开始循环
    for item in range(2,total + 1):
        next_page(item)
    browser.close()

if __name__ == '__main__':
    main()