# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LsscraItem(scrapy.Item):
    # define the fields for your item here like:
     articletype= scrapy.Field()
     authimg=scrapy.Field()
     authnickname = scrapy.Field()
     comment= scrapy.Field()
     createtime= scrapy.Field()
     pv=scrapy.Field()
     remarks=scrapy.Field()
     thumburl=scrapy.Field()
     title=scrapy.Field()
     top=scrapy.Field()
     articlecontent=scrapy.Field()
     quoteurl = scrapy.Field()  
     pass
