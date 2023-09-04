# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class TopkarirsearchSpider(scrapy.Spider):
    name                 = 'topkarirsearch'
    allowed_domains      = ['topkarir.com']
    start_urls           = ['https://www.topkarir.com/lowongan']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1           
        
        #if int(page_number) == 194: 
            #page_number = 194
        #elif int(page_number) >= 1: 
            #page_number = int(page_number) + 1

        data_scrap       = response.xpath('//div[@class="col xl3 l4 m6 s12"]/div[@class="job-card z-depth-3"]/div[@class="body"]/div[@class="caption"]/div[@class="job-title"]/a')
        
        yield {'site': len(data_scrap)}
        for row in data_scrap:                       
            url          = row.xpath('@href').extract_first()                         
            ##next_url     = "https://www.karir.com" + url            
            yield Request(url, callback=self.parse_page,meta={'url': url})

        #next_page     = "https://www.jobs.id/lowongan-kerja?kata-kunci=indonesia&halaman="+ str(page_number)
        
        #yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
    def parse_page(self, response):
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'jobs.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- DOMAIN OF JOBS
            temp_domain_of_jobs = response.xpath('//div[@id="detail-comprof"]/text()').extract()[2]
            domain_of_jobs = temp_domain_of_jobs.strip('\xa0\r\n          ')
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            temp_job_title      = response.xpath('//div[@class="jobtitle"]/text()').extract_first()
            job_title = temp_job_title.strip();
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = response.xpath('//td[@class="jobval"]/text()').extract()[1]            
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
        # -------------------------------------------------------------------------------------------- LOCATION
            temp_location = response.xpath('//div[@id="detail-comprof"]/text()').extract()[1]
            location = temp_location.strip('\xa0\r\n          ')
            
        # -------------------------------------------------------------------------------------------- SALARY
            salary = None               
            temp_salary = response.xpath('//td[@class="jobval"]/text()').extract()[3]
            salary = temp_salary.strip();
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION LEVEL
            qualification_level = response.xpath('//td[@class="jobval"]/text()').extract()[2]
        
        
        # -------------------------------------------------------------------------------------------- My SQL    
            
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="paper_one"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `topkarir`(`website`, `url`, `date_time`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, domain_of_jobs, job_title, position, experience, location, salary, qualification_level)
            mycursor.execute(sql, val)

            mydb.commit()
        
         # ------------------------------------------------------------------------------- 
            yield {'site': site, 
               'url': url, 
               'date_time' : date_time, 
               'domain_of_jobs' : domain_of_jobs, 
               'job_title' : job_title, 
               'position' : position, 
               'experience' : experience, 
               'location' : location, 
               'salary' : salary, 
               'qualification_level' : qualification_level}
