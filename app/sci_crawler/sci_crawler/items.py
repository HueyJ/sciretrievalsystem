# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SciCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    eid = scrapy.Field()
    aggregationType = scrapy.Field()
    title = scrapy.Field()
    publicationName = scrapy.Field()
    volume = scrapy.Field()
    coverDate = scrapy.Field()
    startingPage = scrapy.Field()
    endingPage = scrapy.Field()
    pageRange = scrapy.Field()
    doi = scrapy.Field()
    openaccess = scrapy.Field()
    pii = scrapy.Field()
    author = scrapy.Field()
    abstract = scrapy.Field()
    subject = scrapy.Field()
    issn = scrapy.Field()
