# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# Import scrapy
import scrapy

# GameItem clas that will be called in SplashSpider.py
class DataItem(scrapy.Item):
    # Declare variables that will be scraped from webapge in SplashSpider.py
    Category = scrapy.Field()
    Seller = scrapy.Field()
    Card_Name  = scrapy.Field()
    Condition = scrapy.Field()
    Price = scrapy.Field()
    Stock = scrapy.Field()
