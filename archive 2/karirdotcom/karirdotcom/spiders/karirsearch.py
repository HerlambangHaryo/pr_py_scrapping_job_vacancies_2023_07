# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

class KarirsearchSpider(scrapy.Spider):
    name                 = 'karirsearch'
    allowed_domains      = ['karir.com']
    start_urls           = ['https://www.karir.com/search']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1   
        
        if int(page_number) >= 4:            
            page_number          = response.xpath('//li[@style="display:inline;"]/a/text()').extract()[6]
        elif int(page_number) == 3:            
            page_number          = response.xpath('//li[@style="display:inline;"]/a/text()').extract()[5]
        elif int(page_number) == 2:            
            page_number          = response.xpath('//li[@style="display:inline;"]/a/text()').extract()[4]
        elif int(page_number) == 1:            
            page_number          = response.xpath('//li[@style="display:inline;"]/a/text()').extract()[3]
        
        
        data_scrap       = response.xpath('//div[@class="opportunity-box"]')
        
        for row in data_scrap:                       
            url          = row.xpath('footer/a[@class="btn --full"]/@href').extract_first()                         
            next_url     = "https://www.karir.com" + url            
            yield Request(next_url, callback=self.parse_page,meta={'url': url})
        
        
   
        
        next_page     = "https://www.karir.com/search?q=&sort_order=newest&job_function_ids=&industry_ids=&degree_ids=&major_ids=&location_id=&location=&salary_lower=0&salary_upper=100000000&page="+ str(page_number) +"&grid=box"
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
    
    def parse_page(self, response):
        url = response.meta.get('url') 
        job              = response.xpath('//h5[@class="title"]/text()').extract_first()        
        
        data_scrap          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()
        
        if len(data_scrap) == 4:
            jurusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[2]
            lulusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
            
        if len(data_scrap) == 5:
            jurusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
            lulusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[4]
        
        
            
        
        yield {'url': url,'job': job,'jurusan': jurusan,'lulusan': lulusan}    
        
        #yield {'url': url,'job': job,'jurusan': len(jurusan)}   
        
