# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RbauctionItem(scrapy.Item):
    # define the fields for your item here like:
    Category = scrapy.Field()
    Sub_Category = scrapy.Field()
    Listing_Title = scrapy.Field()
    Make = scrapy.Field()
    ModelModifier = scrapy.Field()
    InYard = scrapy.Field()
    Hours = scrapy.Field()
    AssetType = scrapy.Field()
    Model = scrapy.Field()
    Year = scrapy.Field()
    SerialNumber = scrapy.Field()
    Images_URL = scrapy.Field()
    Thumbnail_URL = scrapy.Field()
    Listing_URL = scrapy.Field()
    pass
