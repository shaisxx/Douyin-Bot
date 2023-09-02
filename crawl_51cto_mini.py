# -*- coding: utf-8 -*-

import requests

requests.packages.urllib3.disable_warnings()

url = 'https://exam.51cto.com/ruankao.php/v1/chapter/index'

headers = {
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
    'user-sign': 'DgZDExYRA1N1QX5WUnYTQGZ0Y1IBQXpBKDxzKTwLFFAAJQ0WHFd8W0BTfmAmTxIBd3JsIj9ndBw3agFUVwUBVlUC',
    'user-token': 'UFELUFddD1Y6Q0oHU1teBlIGVVNeCgRSaxRPUgUGWgYHUVhTXV0GAToCAlJXCVNXUg',
    'user-subject': '240',
    'device-type': 'a'
}

def

if __name__ == '__main__':

    s = requests.Session()
    response = s.get(url, headers=headers, allow_redirects=False, verify=False)
    print(response.text)
