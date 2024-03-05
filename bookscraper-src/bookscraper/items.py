# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()


class ChartascraperItem(scrapy.Item):
    url = scrapy.Field()
    signatory = scrapy.Field()
    organizational_size = scrapy.Field()
    federal_state = scrapy.Field()
    segment = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    street = scrapy.Field()
    city = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()