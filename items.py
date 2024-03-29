# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Chrono24Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    #link = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    reference = scrapy.Field()
    model = scrapy.Field()
    material = scrapy.Field()
    condition = scrapy.Field()
    dial = scrapy.Field()

    pass
