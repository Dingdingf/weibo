# -*- coding: utf-8 -*-
import re

from scrapy import Spider, FormRequest, Request

from weibo_02.items import weibo_user_data


class ExampleSpider(Spider):
    myHeader = {"Cookie":
                    ""}  # 换成自己的cookie
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    user_id = 2443765844
    URL = 'https://weibo.cn/u/%d?filter=1'% (user_id)

    def start_requests(self):
        yield FormRequest(self.URL,callback=self.call_index)

    def call_index(self, response):
        Usr_id = self.user_id
        Usr_Certification = False
        Usr_name = response.xpath("/html/head/title/text()").extract()[0][:-3]
        cf = response.xpath('//div[@class="ut"]/span[@class="ctt"]/text()').extract()
        for cf_ in cf:
            if '认证：' in cf_:
                Usr_Certification =True
        Usr_follows = int(response.xpath("//div[@class='tip2']/a[1]/text()").extract()[0][3:-1])
        Usr_fans =int( response.xpath("//div[@class='tip2']/a[2]/text()").extract()[0][3:-1])
        Usr_mp = int (response.xpath("//input[@name='mp']")[0].attrib["value"])
        Usr_weibo_num = 0  # 两年内的原创数
        Usr_repost_num = 0  # 两年内的转发数

        # for page in range(int(Usr_mp)):
        #     yield FormRequest("https://weibo.cn/u/%d?filter=1&page=%d" % (self.user_id, page+1),
        #                       callback=self.get_weibo_num)
        weibo_item = weibo_user_data()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                pass
        for page in range(Usr_mp):
            yield Request("https://weibo.cn/u/%d?filter=1&page=%d" % (self.user_id, page+1),callback=self.get_weibo_num,meta={"weibo_item":weibo_item})
            print("https://weibo.cn/u/%d?filter=1&page=%d" % (self.user_id, 1))



    def get_weibo_num(self,response):
        weibo_item = response.meta["weibo_item"]

        div = response.xpath('//div[contains(@id,"M_")]/div[last()]/span[@class="ct"]/text()').extract()
        num = response.xpath('//div[contains(@id,"M_")]/div[last()]/a[contains(@href,"https://weibo.cn/repost/")]/text()'
                             ).extract()

        for div_ in range(len(div)):
            a = "".join(div[div_].split())
            if '-'in a:
                date = re.findall('(.*?)-(.*?)-',a)
                if (int(date[0][0]) <= 2017) and (int(date[0][1]) < 3):
                    pass
                else:
                    weibo_item['Usr_weibo_num'] += 1
                    weibo_item['Usr_repost_num'] += int(num[div_][3:-1])
            else:
                weibo_item['Usr_weibo_num'] += 1
                weibo_item['Usr_repost_num'] += int(num[div_][3:-1])
                # self.repost_num += int (num[div_][3:-1])
                # self.weibo_num += 1

        yield weibo_item