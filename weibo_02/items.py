# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Weibo02Item(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class weibo_user_data(Item):
    Usr_name = Field() #用户名字
    Usr_id = Field() #用户ID
    Usr_Certification = Field() #认证
    Usr_follows = Field() #关注者数
    Usr_fans = Field() #粉丝数
    Usr_mp = Field() #原创总页