# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class JobstreetsearchSpider(scrapy.Spider):
    name                 = 'jobstreetpage'
    allowed_domains      = ['jobstreet.co.id']
    start_urls           = ['https://www.jobstreet.co.id/id/job/marketing-plywood-3278958?fr=J&searchRequestToken=6dbf5676-568e-4ee2-f8e9-a9609cb0b730&sectionRank=1']
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'jobstreet.co.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//div[@class="company_name"]/a/text()').extract_first()              
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h1[@class="job-position"]/text()').extract_first()            
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            temp_experience = response.xpath('//span[@id="years_of_experience"]/text()').extract_first()  
            experience = temp_experience.strip()
            
        # -------------------------------------------------------------------------------------------- LOCATION
            temp_location = response.xpath('//span[@class="single_work_location"]/text()').extract_first() 
            location = temp_location.strip()               
            
        # -------------------------------------------------------------------------------------------- SALARY
            salary_1 = response.xpath('//script/text()').re(".*JobAd.Salary.*")
            salary_2 = str(salary_1).split('JobAd.Salary')
            salary_3 = salary_2[1].split('":"')
            salary_4 = salary_3[1].split('"};\']')
            salary = salary_4[0]
            
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

