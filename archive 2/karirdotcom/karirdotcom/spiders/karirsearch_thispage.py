# -*- coding: utf-8 -*-
import scrapy


class KarirsearchThispageSpider(scrapy.Spider):
    name = 'karirsearch_thispage'
    allowed_domains = ['karir.com']
    start_urls = ['https://karir.com/opportunities/1085547']

    def parse(self, response):
        job = response.xpath('//h5[@class="title"]/text()').extract_first()        
        jurusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[4]
        lulusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
        yield {'job': job,'jurusan': jurusan,'lulusan': lulusan} 
        
        #job              = response.xpath('//h5[@class="title"]/text()').extract_first()
        #jurusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[4]
        #lulusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[5]
        
        #jurusan          = ''
        #lulusan          = ''
        
        #count = 0        
        #data_scrap       = response.xpath('//div[@class="b-opportunity-show__aside__info"]')
        
        #for row in data_scrap: 
            #count+1
            #if count == 4:                
                #jurusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract_first()
            #if count == 5:                
                #lulusan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract_first()
        
        
        #yield {'job': job,'jurusan': jurusan,'lulusan': lulusan}    
        
        #yield {'url': url,'job': job,'jurusan': jurusan}   
