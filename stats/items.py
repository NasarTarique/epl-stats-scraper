# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class StatsItem(scrapy.Item):
    name = scrapy.Field()
    position  = scrapy.Field()
    team = scrapy.Field()
    images = scrapy.Field()
    ictrank = scrapy.Field()
    price  = scrapy.Field()
    form  = scrapy.Field()
    totalpoints = scrapy.Field()
    ictindexpos = scrapy.Field()
    gameweekdata = scrapy.Field()
    prevseason = scrapy.Field()
    image_urls = scrapy.Field()
