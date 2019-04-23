# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SciCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    load_date = scrapy.Field()
    link = scrapy.Field()
    identifier = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    creator = scrapy.Field()
    publicationName = scrapy.Field()
    volume = scrapy.Field()
    coverDate = scrapy.Field()
    startingPage = scrapy.Field()
    endingPage = scrapy.Field()
    doi = scrapy.Field()
    openaccess = scrapy.Field()
    pii = scrapy.Field()
    author = scrapy.Field()
