import os

import scrapy

from github_search.items import GithubSearchItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    keyword = os.environ.get('KEYWORD') or 'crawlab'
    start_urls = [f'https://github.com/search?q={keyword}']

    def parse(self, response: scrapy.http.Response, **kwargs):
        for item in response.css('ul.repo-list > li.repo-list-item'):
            name = item.css('.f4.text-normal > a::text').extract_first()
            yield GithubSearchItem(
                name=name,
            )

        next_url = response.css('a.next_page::attr(href)').extract_first()
        if next_url is not None:
            yield scrapy.Request(
                url=f'https://github.com{next_url}',
            )
