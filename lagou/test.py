import requests
from pyquery import PyQuery as pq
COOKIE = 'user_trace_token=20180220204204-7427579d-163b-11e8-8c05-525400f775ce; LGUID=20180220204204-74275b44-163b-11e8-8c05-525400f775ce; JSESSIONID=ABAAABAAAGFABEFC83397E3C1537141FFC2DE568CE586B0; _putrc=F987EFAA75AFE9FC; login=true; unick=%E9%9B%B7%E5%A4%A9%E5%A4%AB; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=9c627c76a2f41945ddc4992032788fa41f9593b5e9e2e280; TG-TRACK-CODE=search_code; SEARCH_ID=f0db57ada2e1494d8883ffdaf7444a83; index_location_city=%E6%B7%B1%E5%9C%B3; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519130527,1519133453,1519259359; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519264230; _gid=GA1.2.1865041969.1519130658; _ga=GA1.2.895092426.1519130525; LGSID=20180222093230-3fadb7f3-1770-11e8-b085-5254005c3644; LGRID=20180222095028-c21fd9fd-1772-11e8-8cf9-525400f775ce'

def request_index_search(positionId):
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
        'User-Agent' : 'Mozilla/5.0 Chrome/58.0.3029.81 Safari/537.36',
    }
    try:
        res = requests.get(url, headers=headers, allow_redirects=False)
        if res.status_code == 200:
            print('get detail url succeed', url)
            res.encoding = res.apparent_encoding
            return res.text
        else:
            print('get detail url failed', res.status_code, url)
            return None
    except ConnectionError as e:
        print('get url error:', e.args, url)
        return None

def parse_url_detail(html):
    doc = pq(html)
    position_description = doc('#job_detail > dd.job_bt > div').text()
    return position_description


def main():
    positionId = '498090'
    html = request_index_search(positionId)
    print(html)
    detail = parse_url_detail(html)
    print(detail)

if __name__ == '__main__':
    main()
