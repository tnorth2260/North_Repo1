# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Class to be called from spider
class DataItem(scrapy.Item):

    # Variables for data to be scrapped
    Set = scrapy.Field()
    Card_Name = scrapy.Field()
    Condition = scrapy.Field()
    Quantity = scrapy.Field()
    Buy_Price = scrapy.Field()
