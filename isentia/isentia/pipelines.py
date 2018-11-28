# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

import pymongo


class MongoPipeline(object):

    collection_name = 'cleansed'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get(
                'MONGO_URI', os.environ.get('MONGO_URI')),
            mongo_db=crawler.settings.get(
                'MONGO_DATABASE', 'articles')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        Find item in database by url: update existing items or insert new
        items (upsert).
        """
        document = {}
        for key, value in dict(item).items():
            if key == 'sub_heading':
                document[key] = value
            else:
                document[key] = value[0]
        self.db[self.collection_name].update(
            {'url': document['url']},
            document,
            upsert=True)
        return item
