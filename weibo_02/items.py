# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class weibo_user_data(Item):

    Usr_name = Field() #用户名字
    Usr_id = Field() #用户ID
    Usr_Certification = Field() #认证
    Usr_follows = Field() #关注者数
    Usr_fans = Field() #粉丝数
    Usr_mp = Field() #原创总页
    Usr_weibo_num = Field()  #两年内的原创数
    Usr_repost_num = Field() #两年内的转发数
