# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class GokarirsearchSpider(scrapy.Spider):
    name                 = 'urbanhiresearch'
    allowed_domains      = ['www.urbanhire.com']
    start_urls           = ['https://www.urbanhire.com/jobs?page=1']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1   
        
        data_scrap       = response.xpath('//li[contains(@class, " ")]')
        
        for row in data_scrap:              
            # -------------------------------------------------------------------------------------------- URL
            url          = row.xpath('div[@class="desktop-listing-content"]/div[@class="noMP col-md-7 col-sm-7 col-xs-7"][1]/a[1]/@href').extract_first()   
            
            # -------------------------------------------------------------------------------------------- SITE
            site = 'gokarir.com'
            
            # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")   
            
            # -------------------------------------------------------------------------------------------- COMPANY
            company = row.xpath('//div[@class="listing-info"]/span[@class="opaque"][1]/text()').extract_first() 
            
            # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
            # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = row.xpath('div[@class="desktop-listing-content"]/div[@class="noMP col-md-7 col-sm-7 col-xs-7"][1]/a[2]/div[@class="listing-title"]/text()').extract_first().strip()   
            
            # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
            # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
            # -------------------------------------------------------------------------------------------- LOCATION
            location = row.xpath('//div[@class="listing-info"]/span[@class="opaque"][2]/text()').extract_first()             
            
            # -------------------------------------------------------------------------------------------- SALARY
            salary = row.xpath('div[@class="desktop-listing-content"]/div[@class="noMP col-md-5 col-sm-5 col-xs-5"][1]/div[@class="listing-type"]/span[@class="list-salary"]/text()').extract_first()

            # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = None 
            
            # -------------------------------------------------------------------------------------------- MY SQL Connection
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="copy_tesis_one"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `gokarir`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`, `page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary, qualification_level, page_number)
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
                   'page' : page_number}
            
        if int(page_number) == 283: 
            page_number = 283
        elif int(page_number) >= 1: 
            page_number = int(page_number) + 1            
        
        next_page     = "https://gokarir.com/jobs?p=" + str(page_number)     
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
 