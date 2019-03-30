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
    user_id = 3217179555
    URL = 'https://weibo.cn/u/%d?filter=1'% (user_id)
    url_page = []
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
        Usr_id = 3217179555
        Usr_Certification = False
        Usr_name = response.xpath("/html/head/title/text()").extract()[0]
        cf = response.xpath('//div[@class="ut"]/span[@class="ctt"]/text()').extract()
        for cf_ in cf:
            if '认证：' in cf_:
                Usr_Certification =True
        Usr_follows = response.xpath("//div[@class='tip2']/a[1]/text()").extract()[0][3:-1]
        Usr_fans = response.xpath("//div[@class='tip2']/a[2]/text()").extract()[0][3:-1]
        Usr_mp = response.xpath("//input[@name='mp']")[0].attrib["value"]
        # for page in range(int(Usr_mp)):
            # self.url_page.append("https://weibo.cn/u/%d?filter=1&page=%d" % ( self.user_id, page + 1))

        # yield FormRequest("https://weibo.cn/u/%d?filter=1&page=%d" % (self.user_id,13),
        #                   callback=self.get_weibo_num)

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


