# -*- coding: utf-8 -*-
import re

from scrapy import Spider, FormRequest, Request

from weibo_02.items import weibo_user_data
from weibo_02.settings import FAND_UID, REDIS_WEBSIT, REDIS_TYPE, REDIS_DB


class ExampleSpider(Spider):

    name = 'weibo'
    allowed_domains = ['weibo.cn']
    """
        top_url  主页地址
    """
    top_url = 'https://weibo.cn/pub/topmblog'
    def start_requests(self):
        from weibo_02.spiders.Rides_tool import Redis_tool
        self.db = Redis_tool(REDIS_DB)
        self.db.set_type_website(REDIS_TYPE,REDIS_WEBSIT)
        if FAND_UID :
            yield FormRequest(self.top_url,callback=self.get_id)
        else:
            self.uid_list =self.db.usernames()
            for uid in self.uid_list:
                url = 'https://weibo.cn/u/%d?filter=1'% (int(uid))
                yield FormRequest(url, callback=self.call_index,meta={"uid":int(uid)})
    def get_id(self,response):
        urls = response.xpath('//div[contains(@id,"M_")]/div/a[@class="nk"]/@href').extract()
        for url in urls:
            yield Request(url,callback=self.get_id_next)

    def get_id_next(self,response):
        urls =response.xpath("//div[@class='tip2']/a[contains(@href,'/follow')]/@href").extract()
        mp = response.xpath("//input[@name='mp']")[0].attrib["value"]

        for url in urls:
            uid = re.findall('/(.*?)/',url)
            self.db.set_data(uid[0],0)
            # print('https://weibo.cn'+url)
            for page in range(5):
                data = {
                    'mp':mp,
                    'page':str(page)
                }
                yield FormRequest(url="https://weibo.cn"+url,callback=self.get_follow_id,formdata=data)
    def get_follow_id(self,response):
        urls = response.xpath('//a[contains(@href,"cn/u/")]/@href').extract()
        for url in urls:
            uid = re.findall('u/(.*?)$', url)
            self.db.set_data(uid[0], 0)

    def call_index(self, response):
        Usr_id = response.meta["uid"]
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

        weibo_item = weibo_user_data()
        for field in weibo_item.fields:
            try:
                weibo_item[field] = eval(field)
            except NameError:
                pass
        for page in range(Usr_mp):
            yield Request("https://weibo.cn/u/%d?filter=1&page=%d" % (Usr_id ,page+1),callback=self.get_weibo_num,meta={"weibo_item":weibo_item})



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
          
        yield weibo_item