import os

import scrapy

from bookdepository.items import BookItem


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.bookdepository.com']
    keyword = os.environ.get('KEYWORD') or 'tech'
    start_urls = [f'https://www.bookdepository.com/search?searchTerm={keyword}']

    def parse(self, response: scrapy.http.Response, **kwargs):
        for item in response.css('.book-item'):
            title = item.css('.item-info h3.title a::text').extract_first()
            author = item.css('.item-info p.author a > span::text').extract_first()
            price = item.css('.item-info .sale-price::text').extract_first()
            published_date = item.css('.item-info p.published::text').extract_first()
            yield BookItem(
                title=title,
                author=author,
                price=price,
                published_date=published_date,
            )

        next_url = response.css('li.next a::attr(href)').extract_first()
        yield scrapy.Request(
            url=f'https://www.bookdepository.com{next_url}',
        )
