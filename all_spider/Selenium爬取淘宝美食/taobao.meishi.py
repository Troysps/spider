from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *

import re
from pyquery import PyQuery as pq
import pymongo

client = pymongo.MongoClient(MONGO_URL) # 申明一个mongodb对象
db = client[MONGO_DB] # 数据库

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 30)

def search_delifood(URL, KEYWORD):

    browser.get(URL)
    enter = wait.until(
        EC.presence_of_element_located((By.ID, "q"))
    )
    click = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
    )
    enter.send_keys('美食')
    click.click()

    total_pages = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
    )
    pattern = re.compile('(\d+)')
    pagesnum = re.search(pattern, total_pages.text).group(1)
    print(pagesnum)
    
    parse_html()
    return int(pagesnum)
#except TimeoutError:
 #   print('模拟搜索关键字失败 TIME OUT', URL, KEYWORD)
  #  return search_delifood(URL, KEYWORD)

def parse_scroll_page(START_PAGE,pagenum):
    try:
        items = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist > div > div"))
        )
        enter = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        click = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        for page in range(START_PAGE, pagenum+1):
            enter.clear()
            enter.send_keys(page)
            click.click()
            
            print(browser.current_url)
            parse_html()
    except:
        print('Scorll Error TIME OUT', page, browser.current_url)
        print(page)
        return parse_scroll_page(page, pagenum)
    

def parse_html():
#  try:
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
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
        save_to_mongoDB(product)

#    except:
#        print('html parse error')
#        return parse_html()

def save_to_mongoDB(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储成功', result)
            return True
    except Exception:
        print('存储失败', result)

def main(URL, KEYWORD):
    total_pages = search_delifood(URL, KEYWORD)
    parse_scroll_page(START_PAGE, total_pages)
    
if __name__ == '__main__':
    main(URL, KEYWORD)
    browser.close()
    
