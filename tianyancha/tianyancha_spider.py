# !/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Project: TianYanCha Spider

@anthor: Troy
@email: ots239ltfok@gmail.com
"""

"""
项目流程
p1: 模拟登陆 https://www.tanyancha.com/login
p2: 跳转搜索界面 输入公司全名进行搜索 并点击跳转
p3: 分析html页面 获取数据
p4: 循环p2 p3
p5: 将数据存储到mongoDB
"""

"""
技术路径: selenium requests pyquery pymongo
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import requests
from requests.exceptions import ConnectionError

from pyquery import PyQuery as pq
import random
import time
import pymongo



# 模拟登陆
LOGIN_URL = 'https://www.tianyancha.com/login'
CONTACTPHONE = '17670626583'
CONTACTWORD = 'HCH520LTF'
proxy = None
MAX_COUNT = 30
COOKIE = 'TYCID=f51bbfa0163e11e8b7645b26a3895c0a; undefined=f51bbfa0163e11e8b7645b26a3895c0a; ssuid=2659455709; RTYCID=9ff40079109d488199d6a33cf4008d9a; aliyungf_tc=AQAAAHhsmyIBmQoASsn6K/wz8dOSmhPX; csrfToken=w1TUipej9167wJde6kctpxRv; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzY3MDYyNjU4MyIsImlhdCI6MTUxOTM3MjYzMCwiZXhwIjoxNTM0OTI0NjMwfQ.sdmW-8FnqhEqJ6vsaaOtVMJFE3SsiBre8M-5GguCmk8f10YuQ8FmOOlKv_h404WBj9vFiK3UZvB4JUMu2Uaamg%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217670626583%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzY3MDYyNjU4MyIsImlhdCI6MTUxOTM3MjYzMCwiZXhwIjoxNTM0OTI0NjMwfQ.sdmW-8FnqhEqJ6vsaaOtVMJFE3SsiBre8M-5GguCmk8f10YuQ8FmOOlKv_h404WBj9vFiK3UZvB4JUMu2Uaamg; _csrf=mB9PiOb/jUSF9Llhcc4zaw==; OA=ujsbLhd1990yWYi1D8KXogt+1foN95KkgUwcZ+8ywOah9z4y2kGW09B9b92XMhnM; _csrf_bk=5920db2c1d644b04bfd4747a74faa2c8; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1519275354,1519275370,1519277383,1519348592; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1519372697'
UA = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"]
MONGO_URL = 'localhost'
MONGO_DB = 'job_related_companies'
MONGO_TABLE = 'ShenZhen_DATAanlysis'


client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

browser = webdriver.Firefox()
browser.maximize_window()
def tianyancha_login(LOGIN_URL):
    try:
        browser.get(LOGIN_URL)
        contactphone = WebDriverWait(browser, 200).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input'))
        ).send_keys(CONTACTPHONE)
        contactword = WebDriverWait(browser, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.pb40.position-rel > input'))
        ).send_keys(CONTACTWORD)
        login_click = WebDriverWait(browser, 200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#web-content > div > div > div > div.position-rel.container.company_container > div > div.in-block.vertical-top.float-right.right_content.mt50.mr5.mb5 > div.module.module1.module2.loginmodule.collapse.in > div.modulein.modulein1.mobile_box.pl30.pr30.f14.collapse.in > div.c-white.b-c9.pt8.f18.text-center.login_btn'))
        ).click()
        print(browser.current_url)
    except TimeoutException:
        print('模拟登陆失败', LOGIN_URL)
        return tianyancha_login(LOGIN_URL)
    
def search_company(companyFullName):
    try:
        search_enter = WebDriverWait(browser, 200).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="home-main-search"]'))
        ).send_keys(companyFullName)
        search_click = WebDriverWait(browser, 200).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="web-content"]/div/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/span'))
        ).click()

        html = browser.page_source
        doc = pq(html)
        com_name = doc('#web-content > div > div > div > div.col-9.search-2017-2.pr15.pl0 > div.b-c-white.search_result_container > div:nth-child(1) > div.search_right_item.ml10 > div:nth-child(1) > a > span').text()
        
        if com_name == companyFullName:
            com_href = doc('#web-content > div > div > div > div.col-9.search-2017-2.pr15.pl0 > div.b-c-white.search_result_container > div:nth-child(1) > div.search_right_item.ml10 > div:nth-child(1) > a').attr.href
            print('get company url:', com_href)
            
            return com_href
        else:
            print('CompanyFullName is wrong', companyFullName)
            browser.back()
            return None
    except TimeoutError as e:
        print('Time Out', e.args)
        return search_company(companyFullName)



def browser_com_href(url):
    browser.get(url)
    # 公司天眼查链接
    tianyancha_url = url
    # company_web_top info:attention name phone email connect_url address readma
    # 关注度(浏览量)
    attention = browser.find_element_by_css_selector('#company_web_top > div.companyTitleBox55 > div > div.position-abs.company-pv.c4 > span').text

    get_name = browser.find_element_by_css_selector('div.company_header_width.ie9Style.position-rel > div')
    # companyFullName
    name = get_name.find_element_by_css_selector('div.position-rel > span').text
    # company phone
    phone = browser.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[2]/div[1]/span[2]').text
    # company email
    email = browser.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[2]/div[2]/span[2]').text
    # company connect_url
    connect_url = browser.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[3]/div[1]/a').text
    # company address
    address = browser.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[3]/div[2]/span[2]').text
    # company readme
    readme = browser.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[2]/div[4]/div/span[2]').text
    browser.implicitly_wait(60)
    businessInfo = get_business_info()

    main_staffCount = browser.find_element_by_css_selector('#nav-main-staffCount > span').text
    main_staff_info = get_main_staff()

    main_holderCount = browser.find_element_by_css_selector('#nav-main-holderCount > span.intro-count').text
    main_holderInfo = get_main_holderInfo()
    investCount = browser.find_element_by_css_selector('#nav-main-inverstCount > span').text
    if investCount:
        investInfo = get_investInfo()

    branchCount = browser.find_element_by_css_selector('#nav-main-branchCount > span').text
    if branchCount:
        branchInfo = get_branchInfo()

    companyRongzi_Count = browser.find_element_by_css_selector('#nav-main-companyRongzi > span').text
    if companyRongzi_Count:
        companyRongzi_Info = get_companyRongzi()
    companyTeammember_Count = browser.find_elemnt_by_css_selector('#nav-main-companyTeammember > span').text
    if companyTeammember_Count:
        companyTeam_info = get_companyTeammember()
    companyProduct_Count = browser.find_element_by_css_selector('#nav-main-companyProduct > span').text
    jinpin_Count = browser.find_element_by_css_selector('#nav-main-companyJingpin > span').text
    cpoyRCount = browser.find_element_by_css_selector('#nav-main-cpoyRCount > span').text
    copyrightWorks = browser.find_element_by_css_selector('#nav-main-copyrightWorks > span').text
    main_icpCount = browser.find_element_by_css_selector('#nav-main-icpCount > span').text
    baseInfo = {
        'tianyancha_url' : tianyancha_url,
        'name': name,
        'phone' : phone,
        'email' : email,
        'connect_url' : connect_url,
        'address' : address,
        'readme' : readme,
        'businessInfo' : businessInfo,
        'main_staffCount' : main_staffCount,
        'main_staff_info' : main_staff_info,
        'main_holderCount' : main_holderCount,
        'main_holderInfo' : main_holderInfo,
        'investCount' : investCount,
        'investInfo' : investInfo,
        'companyRongzi_Count' : companyRongzi_Count,
        'companyRongzi_info' : companyRongzi_info,
        'companyTeammember_Count' : companyTeammember_Count,
        'companyTeam_info' : companyTeam_info,
        'companyProduct_Count' : companyProduct_Count,
        'jinpin_Count' : jinpin_Count,
        'cpoyRCount' : cpoyRCount,
        'copyrightWorks' : copyrightWorks,
        'main_icpCount' : main_icpCount
        }
    
    browser.back()
    browser.back()
    return baseInfo

def get_business_info():
    contents = browser.find_elements_by_css_selector('table.table.companyInfo-table.text-center > tbody > tr > td')
    browser.implicitly_wait(60)
    
# 法人信息
    corporate_info = contents[0].find_element_by_css_selector('td > div.company-human-box.position-rel').text
    # 公司状态
    company_status = contents[1].find_element_by_css_selector('td > div.pt10 > div > div.baseinfo-module-content-value.statusType1').text

    # business info
    trs = browser.find_elements_by_css_selector('div.base0910 > table.table.companyInfo-table.f14 > tbody > tr')
    tianyancha_ranking = trs[0].find_element_by_css_selector(' tr > td.text-center > img').get_attribute('alt')
    business_info = {}
    for tr in trs[0:5]:
        business_info[tr.find_element_by_css_selector('tr > td:nth-child(1)').text] = \
                                                          tr.find_element_by_css_selector('tr > td:nth-child(2)').text
        business_info[tr.find_element_by_css_selector('tr > td:nth-child(3)').text] = \
                                                          tr.find_element_by_css_selector('tr > td:nth-child(4)').text
                                                          
    business_info[trs[5].find_element_by_css_selector('tr > td:nth-child(1)').text] = \
                                                          trs[5].find_element_by_css_selector('tr > td:nth-child(1)').text

    business_scope1 = trs[6].find_element_by_css_selector('tr > td:nth-child(2) > span > span.js-shrink-container > span:nth-child(1)').text
    business_scope2 = trs[6].find_element_by_css_selector('tr > td:nth-child(2) > span > span.js-shrink-container > span:nth-child(2)').text

    if business_scope1 > business_scope2:
        business_info['business_scope'] = business_scope1.strip('.')
    else:
        business_info['business_scope'] = business_scope2.strip('.')
        
    
    result = {
        'corporate_info' : corporate_info,
        'company_status' : company_status,
        'tinyancha_ranking' : tianyancha_ranking,
        'business_info' : business_info
        }
    return result

def get_main_staff():
    """
    get main staff info:position staffName staff_resource
    """
    mainStaffs = browser.find_elements_by_css_selector('div#_container_staff > div > div > div.staffinfo-module-container')

    main_staff_info = {}
    for m in mainStaffs:
        main_staff_info[m.find_element_by_css_selector('div.staffinfo-module-container > div > div:nth-child(1) > span').text] = \
                                                                                       m.find_element_by_css_selector('div.staffinfo-module-container > div > a').text
        main_staff_info[m.find_element_by_css_selector('div.staffinfo-module-container > div > a').text] = \
                                                                                       m.find_element_by_css_selector('div.staffinfo-module-container > div > div > a.point').text
    return main_staff_info

def get_main_holderInfo():
    
    trs = browser.find_elements_by_css_selector('div#_container_holder > div > table.table.companyInfo-table > tbody > tr')
    main_holderInfo = {}
    for tr in trs:
        main_holderInfo['holderName'] = tr.find_element_by_css_selector('tr > td:nth-child(1) > a').text
        # 出资比例
        main_holderInfo['funded_ratio'] = tr.find_element_by_css_selector('tr > td:nth-child(2) > div > div > span').text
        # 认缴出资
        main_holderInfo['subscription_contri'] = tr.find_element_by_css_selector('tr > td:nth-child(3) > div > span').text
        # holder company
        main_holderInfo['holder_resource'] = tr.find_element_by_css_selector('tr > td:nth-child(1) > div > a').text
    return main_holderInfo

def get_investInfo():
    investInfo = []
    while True:
        
        trs = browser.find_elements_by_css_selector('div#_container_invest > div > div > table > tbody > tr')
        #js="window.scrollTo(0,4000);"
        #browser.execute_script(js)
        #browser.find_element_by_xpath('//*[@id="_container_invest"]/div/div[2]/ul/li[5]/a').click()
        
    
        #ActionChains(browser).click(click_next).perform()
        for tr in trs:
            invest = {}
            invest['被投资公司名称'] = tr.find_element_by_css_selector('tr > td:nth-child(1) > a > span').text
            invest['被投资法定代表人'] = tr.find_element_by_css_selector('tr > td:nth-child(2) > span').text
            invest['注册资本'] = tr.find_element_by_css_selector('tr > td:nth-child(3) > span').text
            invest['投资数额'] = tr.find_element_by_css_selector('tr > td:nth-child(4) > span').text
            invest['投资占比'] = tr.find_element_by_css_selector('tr > td:nth-child(5) > span').text
            invest['注册时间'] = tr.find_element_by_css_selector('tr > td:nth-child(6) > span').text
            invest['状态'] = tr.find_element_by_css_selector('tr > td:nth-child(7) > span').text
            investInfo.append(invest)
        try:
            js="window.scrollTo(0,4000);"
            browser.execute_script(js)
            browser.find_element_by_xpath('//*[@id="_container_invest"]/div/div/ul/li[@class="pagination-next  "]/a').click()
           # return get_investInfo()
         #   click_next = browser.find_element_by_xpath('//*[@id="_container_invest"]/div/div[2]/ul/li[@class="pagination-next  "]/a')
          #  ActionChains(browser).click(click_next).perform()

            # 不等待的话界面还在加载但是程序已经继续执行，会导致第二页时候找不到element
            time.sleep(1)
            # 显示等待当载入界面不存在时，界面会有一个下滑的过程，此时程序已经继续往下跑，会导致点击不到下一页
            # located里面要用元组形式
            WebDriverWait(browser, 20, 0.5).until_not(EC.presence_of_element_located((By.ID,"_loading_container")))
            #time.sleep(1)
        except Exception as e:
            print(e)
            return investInfo

def get_branchInfo():
    branchInfo = []
    while True:
        trs = browser.find_elements_by_css_selector('div#_container_branch > div > div > table > tbody > tr')

        for tr in trs:
            branch = {}
            branch['企业名称'] = tr.find_element_by_css_selector('tr > td:nth-child(1) > a > span').text
            branch['法定代表人'] = tr.find_element_by_css_selector('tr > td:nth-child(2) > span').text
            branch['状态'] = tr.find_element_by_css_selector('tr > td:nth-child(3) > span').text
            branch['注册时间'] = tr.find_element_by_css_selector('tr > td:nth-child(4) > span').text
            branchInfo.append(branch)

        try:
            js="window.scrollTo(0,5000);"
            browser.execute_script(js)
            browser.find_element_by_xpath('//*[@id="_container_branch"]/div/div/ul/li[@class="pagination-next  "]/a').click()
           # return get_investInfo()
         #   click_next = browser.find_element_by_xpath('//*[@id="_container_invest"]/div/div[2]/ul/li[@class="pagination-next  "]/a')
          #  ActionChains(browser).click(click_next).perform()

            # 不等待的话界面还在加载但是程序已经继续执行，会导致第二页时候找不到element
            time.sleep(1)
            # 显示等待当载入界面不存在时，界面会有一个下滑的过程，此时程序已经继续往下跑，会导致点击不到下一页
            # located里面要用元组形式
            WebDriverWait(browser, 20, 0.5).until_not(EC.presence_of_element_located((By.ID,"_loading_container")))
            #time.sleep(1)
        except Exception as e:
            print(e)
            return branchInfo


def get_companyRongzi():
    companyRongzi_info = []
    trs = browser.find_elements_by_css_selector('div#_container_rongzi > div > div > table > tbody > tr')
    for tr in trs:
        rongzi = {}
        rongzi['时间'] = tr.find_element_by_css_selector('tr > td:nth-child(1) > span').text
        rongzi['轮次'] = tr.find_element_by_css_selector('tr > td:nth-child(2) > span').text
        rongzi['估值'] = tr.find_element_by_css_selector('tr > td:nth-child(3) > span').text
        rongzi['金额'] = tr.find_element_by_css_selector('tr > td:nth-child(4) > span').text
        rongzi['比例'] = tr.find_element_by_css_selector('tr > td:nth-child(5) > span').text
        rongzi['投资方'] = tr.find_element_by_css_selector('tr > td:nth-child(6)').text
        companyRongzi_info.append(rongzi)

    return companyRongzi_info

def get_companyTeammember():
    companyTeam_Info = []
    while True:
        members = browser.find_elements_by_css_selector('div#_container_teamMember > div > div.team-item')
        for member in members:
            team = {}
            team['team-name'] = member.find_element_by_css_selector('div > div.team-left > div.team-name').text
            team['team-position'] = member.find_element_by_css_selector('div > div.team-right > div.team-title').text
            team['team-experience'] = member.find_element_by_css_selector('div > div.team-right > ul > li > span').text
            commpanyTeam_Info.append(team)
            
        try:
            js="window.scrollTo(0,6000);"
            browser.execute_script(js)
            browser.find_element_by_xpath('//*[@id="_container_teamMember"]/div/div/ul/li[@class="pagination-next  "]/a/a').click()
           # return get_investInfo()
         #   click_next = browser.find_element_by_xpath('//*[@id="_container_invest"]/div/div[2]/ul/li[@class="pagination-next  "]/a')
          #  ActionChains(browser).click(click_next).perform()

            # 不等待的话界面还在加载但是程序已经继续执行，会导致第二页时候找不到element
            time.sleep(1)
            # 显示等待当载入界面不存在时，界面会有一个下滑的过程，此时程序已经继续往下跑，会导致点击不到下一页
            # located里面要用元组形式
            WebDriverWait(browser, 20, 0.5).until_not(EC.presence_of_element_located((By.ID,"_loading_container")))
            #time.sleep(1)
        except Exception as e:
            print(e)
            return companyTeam_Info           
    

def save_to_mongoDB(baseInfo):
    if db[MONGO_TABLE].update({'companyFullName':baseInfo['companyFullName']}, {'$set': baseInfo}, True):
        print('存储数据到mongo', baseInfo['companyFullName'])
    else:
        print('保存数据失败', baseInfo['companyFullName'])
    

def main():
    tianyancha_login(LOGIN_URL)
    all_name = ['深圳市腾讯计算机系统有限公司', '广州牧云网络科技有限公司', '大连万达']
    for n in all_name:
        com_href = search_company(companyFullName=n)
        if com_href:
            data = browser_com_href(url=com_href)
            save_to_mongoDB(baseInfo=data)
            
if __name__ == '__main__':
    main()
