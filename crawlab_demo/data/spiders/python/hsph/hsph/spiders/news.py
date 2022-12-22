import scrapy

from hsph.items import HsphItem


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.hsph.harvard.edu']
    start_urls = ['https://www.hsph.harvard.edu/news/hsph-in-the-news/']

    def parse(self, response: scrapy.http.Response, **kwargs):
        for item in response.css('#main > article'):
            yield HsphItem(
                title=item.css('h2.entry-title > a::text').get(),
                url=item.css('h2.entry-title > a::attr("href")').get(),
                date=item.css('.entry-footer > .posted-on > a::text').get(),
                abstract=item.css('.entry-summary > p::text').get(),
            )

        next_page = response.css('.nav-links > a.next.page-numbers')
        if next_page is not None:
            next_page_url = next_page.css('::attr("href")').get()
            yield response.follow(next_page_url, callback=self.parse)
