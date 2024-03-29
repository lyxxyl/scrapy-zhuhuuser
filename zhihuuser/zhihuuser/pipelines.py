# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ZhihuuserPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):
    collection_name = 'scrapy_items'
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db
    @classmethod
    def from_crawler(cls,Crawl):
        return cls(
            mongo_uri=Crawl.settings.get('MONGO_URI'),
            mongo_db=Crawl.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()
    def process_item(self,item,spider):
        self.db['user'].update({'url_token':item['url_token']},dict(item),upsert=True)
        #self.db[self.collection_name].insert_one(dict(item))
        return item
