# !/urs/bin/env python3
# -*- coding: utf-8 -*-

"""
Project: LAGOU Spider

@author: Troy
@email: ots239ltfok@gmail.com
"""
# 项目构架:
# p1: 依据搜索关键词 城市 职业, 爬取索引页, 解析并获取相关岗位url接连
# p2: 解析url链接, 获取数据
# p3: 存储到MongoDB

# 技术路径: requests urllib json re pq pymongo

import requests
from requests.exceptions import ConnectionError

from pyquery import PyQuery as pq
import urllib
import json
import pymongo
import numpy as np
import time
from config import *


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

proxy = None

def started_search_url(start_url, page):
    headers = {
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Cache-Control' : 'no-cache',
        'Connection' : 'keep-alive',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie' : COOKIE,
        'Host' : 'www.lagou.com',
        'Origin' : 'https://www.lagou.com',
        'Pragma' : 'no-cache',
        'Referer' : REFERER,
        'User-Agent' : 'Mozilla/5.0 Chrome/58.0.3029.81 Safari/537.36',
        }
    query_parameters = {
        'city' : CITY,
        'needAddtionalResult' : 'false',
        'isSchoolJob' : '0'
        }
    form_data = {
        'first' : 'false',
        'pn' : page,
        'kd' : KEYWORD
        }
    url = start_url + urllib.parse.urlencode(query_parameters)
    try:
        res = requests.post(url, headers=headers, data=form_data, allow_redirects=False)
        if res.status_code == 200:
            print('get succeed 200, page:', page)
            res.encoding = res.apparent_encoding
            res = json.loads(res.text)
            return res['content']['positionResult']['result']
        else:
            print('get failed, status code:', res.status_code)
            return None
    except ConnectionError as e:
        print('requests error:', e.args)
        return None

def get_base_data(data):
    try:
        companyId = data['companyId']
        companyFullName = data['companyFullName']
        companyShortName = data['companyShortName']
        companySize = data['companySize']
        positionAdvantage = data['positionAdvantage']
        city = data['city']
        latitude = data['latitude']
        longitude = data['longitude']
        stationname = data['stationname']
        subwayline = data['subwayline']
        financeStage = data['financeStage']
        positionName = data['positionName']
        firstType = data['firstType']
        secondType = data['secondType']
        workYear = data['workYear']
        education = data['education']
        district = data['district']
        salary = data['salary']
        positionLables = data['positionLables']
        positionId = data['positionId']
        html = request_index_search(positionId)
        position_description = parse_url_detail(html)
        

        result = {
            'companyId' : companyId,
            'companyFullName' : companyFullName,
            'companyShortName' : companyShortName,
            'positionAdvantage' : positionAdvantage,
            'latitude' : latitude,
            'longitude' : longitude,
            'stationname' : stationname,
            'subwayline' : subwayline,
            'financeStage' : financeStage,
            'positionName' : positionName,
            'firstType' : firstType,
            'secondType' : secondType,
            'workyear' : workYear,
            'education' : education,
            'district' : district,
            'salary' : salary,
            'positionLables' : positionLables,
            'positionId' : positionId,
            'position_description' : position_description
            }
        return result
    except TypeError :
        print('data get error')
        return None


def get_proxy():
    try:
        response = requests.get(PROXIES_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None
    
def request_index_search(positionId):
    global proxy
    url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)
    headers = {
        'Accept' : 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Cache-Control' : 'no-cache',
        'Connection' : 'keep-alive',
        'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie' : COOKIE,
        'Host' : 'www.lagou.com',
        'Pragma' : 'no-cache',
        'User-Agent' : 'Mozilla/5.0 Chrome/58.0.3029.81 Safari/537.36'
        }
    try:
        if proxy:
            proxies = {
                'https' : 'https://' + proxy
                }
            res = requests.get(url, headers=headers, proxies=proxies, allow_redirects=False)
    
        else:
            res = requests.get(url, headers=headers, allow_redirects=False)
        print('Res.status_code:', res.status_code)
        if res.status_code == 200:
            print('get detail url succeed', url)
            res.encoding = res.apparent_encoding
            return res.text
        if res.status_code == 302:
            print('chunkError', res.status_code, url)
            proxy = get_proxy()
            if proxy:
                return request_index_search(positionId)
            else:
                print('proxy is fail')
                return None
    except ConnectionError as e:
        print('get url error:', e.args, url)
        return None

def parse_url_detail(html):
    doc = pq(html)
    position_description = doc('#job_detail > dd.job_bt > div').text()
    return position_description

def save_to_mongoDB(result):
    if db[MONGO_TABLE].update({'positionId' : result['positionId']}, {'$set' : result}, True):
        print('save to mongoDB Succeed', result)
    else:
        print('save to mongoDB Failed', result)
    


def main(pn):
    time.sleep(np.random.randint(0.1, 1))
    datas = started_search_url(start_url=START_URL, page=pn)
    print(datas)
    for data in datas:
        result = get_base_data(data)
        save_to_mongoDB(result)
    

if __name__ == '__main__':
    for pn in range(1, 20):
        main(pn)
    
