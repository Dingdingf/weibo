# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
from numpy import random


class weibo_iteam(object):
    def process_item(self, item, spider):
        # print(item)
        return item

class RedisClient(object):
    def open_spider(self,spider):
        try:
            self.db = redis.StrictRedis(host="127.0.0.1", port=6379, password="", decode_responses=True)
            self.type = "usr_data"
            self.website = "weibo"
        except Exception as e:
            print('Failed to Get Redis!')
            exit(1)

    def close_spider(self,spider):
        # self.db.hkeys(self.name())
        pass
    def name(self):
        """
        获取Hash的名称
        :return: Hash名称
        """
        return "{type}:{website}".format(type=self.type, website=self.website)
    def set_data(self, username, value):
        """
        设置键值对
        :param username: 用户名
        :param value: 密码或Cookies
        :return:
        """
        return self.db.hset(self.name(),username, value)

    def process_item(self, item, spider):
        # print(item)
        # self.db.hset(self.name(), username, value)
        self.set_data(item['Usr_id'], item)
        print(random.choice(self.db.hvals(self.name())))
        # for key in item:
        #     self.set_data(key,item[key])
            # print(key)
