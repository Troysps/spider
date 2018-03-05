#!/usr/bin/env python  
# encoding: utf-8  



"""爬取淘宝美食信息"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.wait import TimeoutException
import re
from pyquery import PyQuery as pq

import pymongo

client = pymongo.MongoClient('localhost')
db = client['taobao']

#使用 Chrome解析网页
browser = webdriver.Chrome()

#使用phantomjs解析网页
#path = 'D://phantomjs//bin//phantomjs.exe'
#browser = webdriver.PhantomJS(executable_path=path,service_args=SERVICE_ARGS)
#browser.set_window_size(1400,900)

wait = WebDriverWait(browser,10)

def search():
    """查询关键词返回总页数"""
    try:
        browser.get('https://www.taobao.com')
        #显示等待使webdriver等待某个条件成立时继续执行，否则在达到最大时长抛出超时异常（TimeoutException）
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#q")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_TSearchForm > div.search-button > button")))
        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > div.total")))
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    """模拟浏览器翻页"""
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit")))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#mainsrp-pager > div > div > div > ul > li.item.active > span"),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#mainsrp-itemlist .items .item")))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('data-src'),
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
        if db['meishi'].insert(result):
            print('存储到MONGODB成功',result)
    except Exception:
        print('存储到MONGODB失败',result)


def main():
    total = search()
    total = int(re.findall(r'共(.*?)页',total)[0])
    for i in range(2,total + 1):
        next_page(i)
    browser.close()

if __name__ == '__main__':
    main()
