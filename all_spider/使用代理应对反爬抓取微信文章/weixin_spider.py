# !/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Project: Weixin Spider Using proxypool

@author: Troy
@email: ots239ltfok@gmail.com
"""

import re
import requests
from requests.exceptions import  ConnectionError
from bs4 import BeautifulSoup
import pymongo
import os
from config import *
from pyquery import PyQuery as pq


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

headers = {
    'cookie': COOKIE,
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'Connection' : 'keep-alive',
    'Host' : 'weixin.sogou.com',
    'Upgrade-Insecure-Requests' : '1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64)'
    }


proxy = None

def get_proxy():
    try:
        url = PROXIES_URL
        res = requests.get(url)
        if res.status_code == 200:
            return res.text
        return None
    except ConnectionError:
        print('ConnectionError')
        return None

def get_index_page(KEYWORD, page):
    params = {
        'query' : KEYWORD,
        'type' : 2,
        'page' : page
        }
    url = BASE_URL + urlencode(params)
    return get_index_html(url)


def get_index_html(url, count=1):
    print('Runing index url', url)
    print('Runing count', count)
    if count >= MAX_COUNT:
        print('Try many times', url)
        return None
    print('proxy', proxy)
    global proxy
    try:
        if proxy:
            proxies = {
                'http' : 'http' + proxy
                }
            res = requests.get(url, all_redirects=False, headers=headers)
        else:    
        res = requests.get(url, allow_redirects=False, headers=headers)
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            return res.text
        if res.status_code == 302:
            print('proxy has been banned', res.status_code)
            if proxy:
                return get_index_page(url, KEYWORD, page)
            else:
                print('proxy is None')
                return None
    except ConnectionError as e:
        print('Error:', e.args)
        count += 1
        proxy = get_proxy()
        return get_index_html(url, count)


def parse_index_page(html):
    doc = pq(html)
    items = doc('.news-list li').items()
    for item in items:
        url = item.find('div > h3 > a').attr('href')
        print(url)

def request_detail_url(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            res.encoding = res.apparent_encoding
            return res.text
        return None
    except ConnectionError:
        return None

def get_data(html):
    doc = pq(html)
    title = doc('#activity-name').text()
    content = doc('#meta_content').text()
    date = doc('#post-date').text()
    nickname = doc('#post-user').text()
    author = doc('#meta_content > em:nth-child(3)').text()
    return {
        'title':title,
        'content':content,
        'date':date,
        'nickname':nickname,
        'author':author
    }


def save_to_mongoDB(data):
    if db[MONGO_TABLE].updata({'title':data['title']},{'$set':data}, True):
        print('保存数据成功', data['title'])
    else:
        print('保存数据失败', data['title'])
    
    
    

def main():
    html = get_index_page(url, KEYWORD, page)
    parse_index_page(html)




if __name__ == '__main__':
    for page in range(8, 100):
        print(page)
        main(url, KEYWORD, page)
