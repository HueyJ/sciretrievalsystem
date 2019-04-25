# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import requests, os, json

class SciCrawlerESPipeline(object):
    def __init__(self):
        self.es_url = "http://" + os.environ.get('ELASTICSEARCH_HOST') + ":"\
                                + os.environ.get('ELASTICSEARCH_PORT')
        self.index_name = os.environ.get('INDEX_NAME')
        self.type_name = os.environ.get('TYPE_NAME')

    def process_item(self, item, spider):
        documentDict = {item["pii"]: dict(item)}
        self.__index(documentDict)
        self.__jsonize(item)


    def __index(self, documentDict):
        bulkDocs = ""
        for id, document in documentDict.items():
            addCmd = {
                "index" : {
                    "_index" : self.index_name,
                    "_type" : self.type_name,
                    "_id" : id
                }
            }
            bulkDocs += json.dumps(addCmd) + "\n" + json.dumps(document) + "\n"
        resp = requests.post(self.es_url + "/_bulk",
                             data=bulkDocs,
                             headers={"Content-Type" : "application/x-ndjson"})

    def __jsonize(self, item):
        with open("../articles/" + item["pii"] + ".json", "wb") as f:
            f.write(b"[\n")
            f.write(json.dumps(dict(item)).encode(encoding='utf-8'))
            f.write(b"\n]")
