# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductscrawlerItem(scrapy.Item):
    name = scrapy.Field(),
    brand = scrapy.Field(),
    price = scrapy.Field(),
    image = scrapy.Field(),
    category = scrapy.Field(),
    unit_text = scrapy.Field(),
    unit_int = scrapy.Field(),
    alldetails = scrapy.Field()
