# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json

import requests


class CookiesMid():

    def __init__(self):
        self.cookies_pool_url = 'http://127.0.0.1:5020/weibo/random'
    def _get_random_cookies(self):
        try:
            respose = requests.get(self.cookies_pool_url)
            if respose.status_code == 200:
                return json.loads(respose.text)
        except ConnectionError:
            return None
    # @classmethod
    # def form_crawler(cls,crawler):
    #     return cls(
    #         cookies_pool_url = crawler.seetings.get('COOKIES_POOL_URL')
    #     )
    def get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get/").content

    def process_request(self,request,spider):
        Cookies = self._get_random_cookies()
        proxy = self.get_proxy()
        retry_count = 5
        if proxy is  not None:
            request.proxies = {"http": "http://{}".format(proxy)}
        if Cookies:
            request.cookies = Cookies
        else:
            print("get_cookies_no")