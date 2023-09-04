# -*- coding: utf-8 -*-
import scrapy


class KarirsearchSpider(scrapy.Spider):
    name = 'karirsearchs'
    allowed_domains = ['karir.com']
    start_urls = ['http://karir.com/search']

    def parse(self, response):
        data_scrap = response.xpath('//div[@class="opportunity-box"]')
        
        for row in data_scrap:                 
            title = row.xpath('header/a[@class="--blue"]/h4[@class="tdd-function-name --semi-bold --inherit"]/text()').extract_first()
            yield {'Title': title}       