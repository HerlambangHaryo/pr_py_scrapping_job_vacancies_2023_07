# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class TopkarirsearchSpider(scrapy.Spider):
    name                 = 'topkarirpage'
    allowed_domains      = ['topkarir.com']
    #start_urls           = ['https://www.topkarir.com/lowongan/detil/pt-jaya-putra-multiguna-freelance-dsign-websitgrafis']
    start_urls           = ['https://www.topkarir.com/lowongan/detil/pt-satu-suara-indonesia-desk-collection']
    
    
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'jobs.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- DOMAIN OF JOBS
            domain_of_jobs = response.xpath('//div[@id="detail-comprof"]/text()').extract()[2]
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            temp_job_title      = response.xpath('//div[@class="jobtitle"]/text()').extract_first()
            job_title = temp_job_title.strip();
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = response.xpath('//td[@class="jobval"]/text()').extract()[1]            
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
        # -------------------------------------------------------------------------------------------- LOCATION
            location = response.xpath('//div[@id="detail-comprof"]/text()').extract()[1]
            
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
