# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    kt=scrapy.Field()
    ws=scrapy.Field()
    qt=scrapy.Field()
    fwhx=scrapy.Field()
    szlc=scrapy.Field()
    jzmj=scrapy.Field()
    hxjg=scrapy.Field()
    tnmj=scrapy.Field()
    jzlx=scrapy.Field()
    fwcx=scrapy.Field()
    jzjg=scrapy.Field()
    zxqk=scrapy.Field()
    thbl=scrapy.Field()
    pbdt=scrapy.Field()
    yslx=scrapy.Field()
    ydlx=scrapy.Field()
    rqjg=scrapy.Field()
    name=scrapy.Field()#区名
    des=scrapy.Field()#描述语言
    totalprice=scrapy.Field()#总价格
    unitprice=scrapy.Field()#平均价格
    gz=scrapy.Field()#关注人数
    jd=scrapy.Field()#经度
    wd=scrapy.Field()#纬度
    xqname=scrapy.Field()#小区名字
    gpsj=scrapy.Field()
    jyqs=scrapy.Field()
    scjy=scrapy.Field()
    fwyt=scrapy.Field()
    fwnx=scrapy.Field()
    cqss=scrapy.Field()
    dyxx=scrapy.Field()
    fbbj=scrapy.Field()
    tu=scrapy.Field()
    city=scrapy.Field()
    pass
