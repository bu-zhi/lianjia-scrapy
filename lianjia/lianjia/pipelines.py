# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

#
# class LianjiaPipeline:
#     def process_item(self, item, spider):
#         print(item)
#         return item


from pymongo import MongoClient


class MongoPipeline(object):
    def __init__(self):
        client = MongoClient(host='45.145.74.209', port= 27017,username="root",password="admin_mima")
        self.db = client['shixi']
        self.coll = self.db['lianjia']  # 获得collection的句柄

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        self.coll.insert_one(postItem)  # 向数据库插入一条记录
        return item  # 会在控制台输出原item数据，可以选择不写