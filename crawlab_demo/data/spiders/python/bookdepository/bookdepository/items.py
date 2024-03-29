# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    price = scrapy.Field()
    published_date = scrapy.Field()
    excerpt = scrapy.Field()
    product_details = scrapy.Field()
