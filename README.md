# weibo
一个微博爬虫
爬取用户信息存入Rides数据库中有微博Cookies池的使用，但未上传。
需要可去Cookies池
https://github.com/Python3WebSpider/CookiesPool.git 

先设置True模式一 爬取热门的的发表人和发布人关注的前五页的ID
设置False 模式二 爬取前面获取的ID的用户信息
包括以下内容。
{
    Usr_name = Field() #用户名字
    Usr_id = Field() #用户ID
    Usr_Certification = Field() #认证
    Usr_follows = Field() #关注者数
    Usr_fans = Field() #粉丝数
    Usr_mp = Field() #原创总页
    Usr_weibo_num = Field()  #两年内的原创数
    Usr_repost_num = Field() #两年内的转发数
}
settings.py 

#切换模式
FAND_UID = False


爬取到的信息
{'Usr_Certification': True,
 'Usr_fans': 9877796,
 'Usr_follows': 2289,
 'Usr_id': 2549228714,
 'Usr_mp': 154,
 'Usr_name': '英国那些事儿',
 'Usr_repost_num': 1941080,
 'Usr_weibo_num': 1534
 }
