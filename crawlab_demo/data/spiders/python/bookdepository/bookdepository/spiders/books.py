import os
from urllib.parse import urljoin

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
            url = urljoin(response.url, item.css('.item-info h3.title a::attr("href")').extract_first())
            image = item.css('.item-img img::attr("data-lazy")').extract_first()
            author = item.css('.item-info p.author a > span::text').extract_first()
            price = item.css('.item-info .sale-price::text').extract_first()
            published_date = item.css('.item-info p.published::text').extract_first()
            book_item = BookItem(
                title=title,
                url=url,
                image=image,
                author=author,
                price=price,
                published_date=published_date,
            )
            yield scrapy.Request(url, callback=self.parse_item, meta={'book_item': book_item})

        next_url = response.css('li.next a::attr(href)').extract_first()
        yield scrapy.Request(
            url=f'https://www.bookdepository.com{next_url}',
        )

    def parse_item(self, response: scrapy.http.Response, **kwargs):
        book_item = response.meta['book_item']
        book_item['excerpt'] = response.css('.item-excerpt::text').extract_first()
        book_item['product_details'] = response.css('.biblio-wrap').extract_first()
        yield book_item
