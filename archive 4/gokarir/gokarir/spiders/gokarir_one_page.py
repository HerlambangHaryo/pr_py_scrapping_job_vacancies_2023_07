# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class GokarirsearchSpider(scrapy.Spider):
    name                 = 'gokarirpage'
    allowed_domains      = ['gokarir.com']
    start_urls           = ['https://gokarir.com/job/12259/junior-product-consultant-di-gadjiancom']
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'gokarir.com'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = None             
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h4[@class="job-detail-headline"]/text()').extract_first().strip()
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
        # -------------------------------------------------------------------------------------------- LOCATION
            location = None    
            
            
        # -------------------------------------------------------------------------------------------- SALARY
            salary = None
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = None  
         
        # -------------------------------------------------------------------------------------------- MY SQL Connection
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
                   'qualification_level' : qualification_level}
