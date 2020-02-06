# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Class that will be called from spider
class DataItem(scrapy.Item):

    # Variables for crawling webpage
    Category = scrapy.Field()
    Card_Name = scrapy.Field()
    Condition = scrapy.Field()
    Buy_Price = scrapy.Field()
    Rarity = scrapy.Field()
    Foil = scrapy.Field()
    Language = scrapy.Field()
