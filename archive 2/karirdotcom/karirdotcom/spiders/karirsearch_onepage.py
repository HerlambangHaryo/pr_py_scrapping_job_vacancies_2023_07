# -*- coding: utf-8 -*-
import scrapy


class KarirsearchOnepageSpider(scrapy.Spider):
    name = 'karirsearch_onepage'
    allowed_domains      = ['karir.com']
    start_urls           = ['https://www.karir.com/search']

    def parse(self, response):
        #data_scrap = response.xpath('//div[@class="opportunity-box"]')
        
        #for row in data_scrap:                 
            #title = row.xpath('header/a[@class="--blue"]/h4[@class="tdd-function-name --semi-bold --inherit"]/text()').extract_first()
            #yield {'Title': title}    
            
        data_scrap = response.xpath('//li[@style="display:inline;"]/a')
        page_number          = response.xpath('//li[@style="display:inline;"]/a/text()').extract()[2]
        
        #yield {'page': len(data_scrap)}
        yield {'page': len(data_scrap),'pagenumber': page_number}
        
        #i = 0
        #while i <  len(data_scrap) - 1:
            #data_scrapa = response.xpath('//li[@style="display:inline;"]/text()').extract()[int(i)]
            #yield {'Title': data_scrapa}
            #i += 1
            
        #for row in data_scrap:
            #data_scrapa = response.xpath('//li[@class="display:inline;"]/text()').extract_first()
            #yield {'Title': data_scrapa}
        
        #for row in data_scrap:                 
            #title = row.xpath('header/a[@class="--blue"]/h4[@class="tdd-function-name --semi-bold --inherit"]/text()').extract_first()
            #yield {'Title': title}