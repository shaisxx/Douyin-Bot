#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'shaisxx'

import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

base_url = "http://www.aii-alliance.org"

'''
@description: 天眼查爬虫主类
@param 
@return: 
'''
class Alliance:

    # 登录URL
    login_url = 'http://www.aii-alliance.org/index/login.html'

    def __init__(self, username, password, headless=False):
        self.username = username
        self.password = password
        self.headless = headless
        #填写信息
        self.driver = self.login(text_login=self.username, text_password=self.password)

    # 登录天眼查 done
    def login(self, text_login, text_password):
        time_start = time.time()

        # 操作行为提示
        logger.info('在自动输入完用户名和密码前，请勿操作鼠标键盘！请保持优雅勿频繁（间隔小于1分钟）登录以减轻服务器负载。')
        chromedriver="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chromedriver)

        # 强制声明浏览器长宽为1024*768以适配所有屏幕
        driver.set_window_position(0, 0)
        driver.set_window_size(1024, 768)
        driver.get(self.login_url)

        # 模拟登陆：Selenium Locating Elements by Xpath
        time.sleep(1)

        driver.find_element_by_xpath("//input[@id='LAY-user-login-username']").click()
        driver.find_element_by_xpath("//input[@id='LAY-user-login-username']").send_keys(self.username)

        driver.find_element_by_xpath("//input[@id='LAY-user-login-password']").click()
        driver.find_element_by_xpath("//input[@id='LAY-user-login-password']").send_keys(self.password)

        # 手工登录，完成验证码
        logger.info('请现在开始操作键盘鼠标，在15s内点击登录并手工完成验证码。批量爬取只需一次登录。')
        time.sleep(15)

        driver.find_element_by_xpath("//button[@id='login']").click()

        cookie = driver.get_cookies()#获取cookie
        jsonCookies = json.dumps(cookie)
        #创建文件保存cookie
        with open('storeCookie.json','w') as f:
            f.write(jsonCookies)
        with open('storeCookie.json','r',encoding='utf-8') as f:
            listCookies=json.loads(f.read())
        cookie = [item["name"] + "=" + item["value"] for item in listCookies]
        cookiestr = '; '.join(item for item in cookie)#提取成headers的cookie字符串形式

        headers = {
            'cookie': cookiestr,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }

        logger.info('还剩5秒。')
        time.sleep(5)

        # 跳转资料下载页面
        driver.find_element_by_xpath("//a[contains(text(),'资料下载')]").click()
        time.sleep(5)

        # 跳转成果资料下载页面
        driver.find_element_by_xpath("//div[contains(text(),'成果资料')]").click()
        time.sleep(5)

        # 进入其他资料
        driver.find_element_by_xpath("//div[contains(text(),'其他资料')]").click()
        time.sleep(5)

        #加载页面
        content = driver.page_source.encode('utf-8')
        divs = BeautifulSoup(content, 'html.parser').find('div', class_='attactent-tab-content active').find('div', class_='attactent-files-list active').find_all('div', class_='attactent-files-item')
        for div in divs:
            file_name = div.find('div', class_='attactent-files-item-name').text
            logger.info(file_name)

            file_url = base_url + div.find('div', class_='attactent-files-item-btn').find('a', class_="attactent-file-down-btn").attrs['href']
            logger.info(file_url)

            try:
                r = requests.get(url=file_url, headers=headers, stream=True)
                with open("1.pdf", "wb") as pdf:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            pdf.write(chunk)
            except Exception as ex:
                logger.error(ex)

            time.sleep(3)

        time.sleep(5)

        logger.info('您的本次登录共用时{}秒。'.format(int(time.time() - time_start)))
        return driver

    def alliance_scrapy(self):
        logger.info("开始资料下载")

if __name__ == "__main__":

    Alliance(username='15210434997', password='sh4499118').alliance_scrapy()
