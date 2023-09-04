# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class LokersearchSpider(scrapy.Spider):
    name                 = 'lokersearch'
    allowed_domains      = ['loker.id']
    start_urls           = ['https://www.loker.id/cari-lowongan-kerja?q&lokasi=0']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1           
        
        data_scrap       = response.xpath('//div[contains(@class, "job-box")]')       
        
        for row in data_scrap:                       
            url          = row.xpath('div[@class="row"]/div[@class="col-md-3"]/div[@class="media "]/div[@class="media-body"]/h3[@class="media-heading h4"]/a/@href').extract_first()
            yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
    
        if int(page_number) == 500: 
            page_number = 500
        elif int(page_number) >= 1: 
            page_number = int(page_number) + 1
            
        next_page     = "https://www.loker.id/cari-lowongan-kerja/page/"+ str(page_number)+"?q&lokasi=0"
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
        
       
           
    def parse_page(self, response):
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'loker.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//span[@itemprop="name"]/text()').extract_first() 
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS 
            domain_of_jobs = response.xpath('//span[@itemprop="occupationalCategory"]/a/text()').extract_first() 
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//span[@itemprop="title"]/text()').extract_first()    
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = response.xpath('//div[@class="row"]/div[@class="col-md-3"][1]/strong/a/text()').extract_first()
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE            
            experience = None
            
        # -------------------------------------------------------------------------------------------- LOCATION
            location = response.xpath('//span[@itemprop="addressLocality"]/a/text()').extract_first()    
            
        # -------------------------------------------------------------------------------------------- SALARY          
            salary = None
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = response.xpath('//span[@itemprop="educationRequirements"]/a/text()').extract_first()                 
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION
            page = response.meta.get('page_number')  
         
        # -------------------------------------------------------------------------------------------- My SQL
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="paper_one"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `loker`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`, `page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary, qualification_level,page)
            mycursor.execute(sql, val)

            mydb.commit()
        # -------------------------------------------------------------------------------------------- 
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