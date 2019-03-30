# -*- coding: utf-8 -*-
import codecs
import csv
import re

import requests
from lxml import etree
from scrapy import Spider,FormRequest


class ExampleSpider(Spider):
    myHeader = {"Cookie":
                    ""}  # 换成自己的cookie
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    URL = 'https://weibo.cn/u/3217179555?filter=1'
    url_page = []
    user_id = 3217179555
    title= ''
    following = 0
    follows = 0
    mp = 0
    Certification = False
    weibo_num =  0
    repost_num = 0
    def start_requests(self):
        yield FormRequest(self.URL,callback=self.call_index)
    def call_index(self, response):
        # fh = codecs.open( "2211781230.html", "w", "UTF-8")
        # fh.write(response.text)
        # fh.close()
        self.Certification = False
        self.title = response.xpath("/html/head/title/text()").extract()[0]
        cf = response.xpath('//div[@class="ut"]/span[@class="ctt"]/text()').extract()
        for cf_ in cf:
            if '认证：' in cf_:
                self.Certification =True
        self.following = response.xpath("//div[@class='tip2']/a[1]/text()").extract()[0][3:-1]
        self.follows = response.xpath("//div[@class='tip2']/a[2]/text()").extract()[0][3:-1]
        self.mp = response.xpath("//input[@name='mp']")[0].attrib["value"]
        for page in range(int(self.mp)):
            self.url_page.append("https://weibo.cn/u/%d?filter=1&page=%d" % ( self.user_id, page + 1))

        yield FormRequest("https://weibo.cn/u/%d?filter=1&page=%d" % (self.user_id,13),
                          callback=self.get_weibo_num)

    def get_weibo_num(self,response):

        div = response.xpath('//div[contains(@id,"M_")]/div[last()]/span[@class="ct"]/text()').extract()
        num = response.xpath('//div[contains(@id,"M_")]/div[last()]/a[contains(@href,"https://weibo.cn/repost/")]/text()'
                             ).extract()
        for div_ in num:
            if '-(.*?)-' in div_:
                print(div_)
            else:
                print(div_)
                # self.repost_num += int (num[div_][3:-1])
                # self.weibo_num += 1


    def toStr(self):
        print(self.title)
        print(self.Certification)
        print(self.following)
        print(self.follows)
        print(self.mp)
        # print(self.url_page)


    def parse(self, response):
        print(response.text)


