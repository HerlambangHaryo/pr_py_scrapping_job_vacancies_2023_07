# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class KarirsearchSpider(scrapy.Spider):
    name                 = 'karirsearch'
    allowed_domains      = ['karir.com']
    start_urls           = ['https://www.karir.com/search']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 0   

        data_scrap       = response.xpath('//div[@class="opportunity-box"]')
        
        for row in data_scrap:                       
            url          = row.xpath('footer/a[@class="btn --full"]/@href').extract_first()                         
            next_url     = "https://www.karir.com" + url            
            yield Request(next_url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
            
        if int(page_number) == 376: 
            page_number = 376
        elif int(page_number) >= 0: 
            page_number = int(page_number) + 1     

        next_page     = "https://www.karir.com/search?q=&sort_order=newest&job_function_ids=&industry_ids=&degree_ids=&major_ids=&location_id=&location=&salary_lower=0&salary_upper=100000000&page="+ str(page_number) +"&grid=box"
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
    def parse_page(self, response):
        url = response.meta.get('url') 
        
        site = 'karir.com'
        
        # -------------------------------------------------------------------------------------------- DATE TIME            
        now = datetime.datetime.now()        
        date_time = now.strftime("%Y-%m-%d %H:%M:%S") 
        
        company = response.xpath('//a[@class="link"]/text()').extract_first()
        
        job_title = response.xpath('//h5[@class="title"]/text()').extract_first()
        
        domain_of_jobs = response.xpath('//li[@class="job--function tooltip__parent"]/text()').extract_first()
        
        location = response.xpath('//li[@class="job--location"]/text()').extract_first()
       
        experience = response.xpath('//li[@class="job--experience"]/text()').extract_first()
        
        salary = response.xpath('//span[@class="salary"]/text()').extract_first()
        
        
        data_scrap          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()
        
        position          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[1]
        
        
        page = response.meta.get('page_number') 
        
        if len(data_scrap) == 4:
            qualification_2          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[2]
            qualification_3          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
            
        if len(data_scrap) == 5:
            qualification_2          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
            qualification_3          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[4]
            
        qualification_level = qualification_2 + ' ' + qualification_3
        
        # -------------------------------------------------------------------------------------------- MY SQL Connection
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="",
          database="paper_one"
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO `karir_new_bb`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`, `page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary, qualification_level, page)
        mycursor.execute(sql, val)

        mydb.commit()
        
        yield {'site': site, 
               'url': url, 
               'date_time' : date_time, 
               'company' : company, 
               'domain_of_jobs' : domain_of_jobs, 
               'job_title' : job_title, 
               'position' : position, 
               'experience' : experience, 
               'location' : location, 
               'salary' : salary, 
               'qualification_level' : qualification_level, 
               'page' : page}
        
