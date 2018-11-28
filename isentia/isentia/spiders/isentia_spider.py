import os

import scrapy
import requests

from isentia.items import IsentiaItem


class IsentiaSpider(scrapy.Spider):
    name = 'isentia'
    start_urls = [
        'https://www.isentia.com/news/blog/ideas',
        'https://www.isentia.com/news/blog/issues-that-matter',
        'https://www.isentia.com/news/blog/viewpoint',
        'https://www.isentia.com/news/blog/access-project'
    ]

    def parse(self, response):
        """
        Parse links to Isentia blog post articles from subject index page and
        follow links to parse article contents.
        """
        for href in response.xpath('//h2//a'):
            yield response.follow(href, callback=self.parse_article)

    def parse_article(self, response):
        """
        Parse contents of Isentia blog post yielding an IsentiaItem.
        """
        item = IsentiaItem()
        item['author'] = 'Isentia',
        item['text'] = self.cleansed(response.css('#main-content')),
        item['url'] = response._url,
        item['headline'] = response.xpath(
            '//h1/text()').extract_first().strip(),
        item['sub_heading'] = response.xpath(
            '//h2/text()').extract_first().strip()
        yield item

    def cleansed(self, content):
        """
        Extract cleansed plaintext from nested html elements.

        XPath expression was inspired by:
        https://stackoverflow.com/questions/26301831/extracting-text-xpath-scrapy
        """
        tokens = content.xpath('descendant-or-self::*/text()').extract()
        return ' '.join([t.strip() for t in tokens if t]).strip()
