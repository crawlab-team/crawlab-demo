import scrapy

from hackernews.items import HackernewsItem


class NewsYcombinatorSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response: scrapy.http.Response, **kwargs):
        for item in response.css('tr.athing'):
            yield HackernewsItem({
                'title': item.css('.titleline > a::text').get(),
                'url': item.css('.titleline > a::attr("href")').get(),
            })
