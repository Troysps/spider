import requests
from pyquery import PyQuery as pq
import random

COOKIE = 'TYCID=f51bbfa0163e11e8b7645b26a3895c0a; undefined=f51bbfa0163e11e8b7645b26a3895c0a; ssuid=2659455709; RTYCID=9ff40079109d488199d6a33cf4008d9a; aliyungf_tc=AQAAAHhsmyIBmQoASsn6K/wz8dOSmhPX; csrfToken=w1TUipej9167wJde6kctpxRv; token=0721bc319b47485981a39d9497a2cefc; _utm=4a54b3dba4e241899aeb3e2a48ad571f; tyc-user-info=%257B%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzYwMjEzNDc5NSIsImlhdCI6MTUxOTQ0MDIzMiwiZXhwIjoxNTM0OTkyMjMyfQ.DKsS_uLSrPcWtuat0ANS9zTGD9ysVezsb66qxCf2Rb-TfK8qcko_yX8FpSv2uBgmNfcIsBksvt-wwL3U2jJRgg%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252217602134795%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNzYwMjEzNDc5NSIsImlhdCI6MTUxOTQ0MDIzMiwiZXhwIjoxNTM0OTkyMjMyfQ.DKsS_uLSrPcWtuat0ANS9zTGD9ysVezsb66qxCf2Rb-TfK8qcko_yX8FpSv2uBgmNfcIsBksvt-wwL3U2jJRgg; _csrf=AWzeWHx/wJanQB5FSMTV/w==; OA=qKZbA3fO5jGSTk6i9p/DVtrzy+Qy7O+b2y2Z8egn+rU=; _csrf_bk=327492fdea3285a54dd0d982499a5003; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1519275370,1519277383,1519348592,1519391521; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1519440237'
UA = ["Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
      "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"]
headers = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'Cache-Control' : 'no-cache',
    'Connection' : 'keep-alive',
    'Cookie' : COOKIE,
    'User-Agent' : random.choice(UA),
    'Referer' : 'https://www.tianyancha.com/search?key=%E8%85%BE%E8%AE%AF&checkFrom=searchBox'
    }


url = 'https://www.tianyancha.com/company/9519792'
res = requests.get(url, headers=headers, allow_redirects=False)
if res.status_code == 200:
    print('get url succeed:', url)
    res.encoding = res.apparent_encoding
    html = res.text
print(res.status_code)
doc = pq(html)
items = list(doc('div.company_header_interior > div > div > span:nth-child(2)').items())

baseInfo = {
    'companyFullName' : doc('div#company_web_top > div > div > div.position-rel > span').text(),
    'attention' : doc('div.position-abs.company-pv.c4').text(),
    'com_phone' : items[0].text(),
    'com_email' : items[1].text(),
    'com_url' : doc('div.company_header_interior > div > div > a').text(),
    'com_address' : items[2].text(),
    'com_readme' : items[-1].text(),
    'boss' : doc('table > tbody > tr > td > div > div.human-top > div.in-block.vertical-top > div > a').text(),
    'boss_company' : doc('table > tbody > tr > td > div > div.human-top > div.in-block.vertical-top > p > span').text(),
    'tianyancha_ranking' : doc('table > tbody > tr > td.text-center > img').attr('alt'),
    'industry' : doc('table > tbody > tr:nth-child(3) > td:nth-child(4)').text(),
    'com_type' : doc('table > tbody > tr:nth-child(2) > td:nth-child(4)').text(),
    'business_scope' : doc('table > tbody > tr > td > span > span > span.js-full-container').text(),
    'main_staffCount' : doc('#nav-main-staffCount > span').text(),
    'main_staff' : doc('div.clearfix > div.staffinfo-module-container > div > a').text(),
    'main_staff_company' : doc('div.clearfix > div.staffinfo-module-container > div > div.in-block > a').text(),
    'main_holderCount' : doc('#nav-main-holderCount > span.intro-count').text(),
    'main_holder' : doc('#_container_holder > div > table > tbody > tr > td > a').text(),
    'main_holder_company' : doc('#_container_holder > div > table > tbody > tr > td > div > a').text(),
    'Funder_ratio' : doc('#_container_holder > div > table > tbody > tr > td > div > div > span').text(),
    'holder_amount' : doc('#_container_holder > div > table > tbody > tr > td > div > span').text(),
    'investment_count' : doc('#nav-main-jigouTzanli > span').text(),
    'investment_info' : doc('#_container_touzi').text(),
    'competitive_count' : doc('#nav-main-companyJingpin > span').text(),
    'competitive_info' : doc('#_container_jingpin').text(),
    'main_products' : doc('#nav-main-productinfo > span').text(),
    'certificateCount' : doc('#nav-main-certificateCount > span').text(),
    'weChatCount' : doc('#nav-main-weChatCount > span').text(),
    'tradeMarkCount' : doc('#nav-main-tmCount > span').text(),
    'patentCount' : doc('#nav-main-patentCount > span').text(),
    'cpoyRCount' : doc('#nav-main-patentCount > span').text(),
    'copyrightWorks' : doc('#nav-main-copyrightWorks > span').text(),
    'icpCount' : doc('#nav-main-icpCount > span').text(),
    }

print(baseInfo)





