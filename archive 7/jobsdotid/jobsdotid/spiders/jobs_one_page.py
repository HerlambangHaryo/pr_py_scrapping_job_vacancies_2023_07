# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector


class JobssearchSpider(scrapy.Spider):
    name                 = 'jobsid_page'
    allowed_domains      = ['jobs.id']
    #start_urls           = ['https://www.jobs.id/lowongan/MjY4MDYz/financial-services-consultant-rifan-financindo-bandung-pt?qt_ref=search&qt_page=37&qt_pos=1']
    start_urls           = ['https://www.jobs.id/lowongan/Mjg4MDg5/operator-manufactur?qt_ref=search&qt_page=1&qt_pos=11']    
    #start_urls           = ['https://www.jobs.id/lowongan/MTc0NzU3/micetour-bet-obaja-international-pt?qt_ref=search&qt_page=1&qt_pos=2']
    
    
    
    
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'jobs.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- DOMAIN OF JOBS
            domain_of_jobs = response.xpath('//a[@class="cyan semi-bold"]/text()').extract_first()
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            temp_job_title = response.xpath('//h1[@class="clear-top bold"]/text()').extract_first()
            job_title      = temp_job_title.strip() 
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            data_scrap       = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"]')
            if(len(data_scrap)) == 3:
                temp_experience = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][1]/h4/span[@class="semi-bold"]/text()').extract_first()
                experience      = temp_experience.strip() 
            
        # -------------------------------------------------------------------------------------------- LOCATION
            location_1 = response.xpath('//span[@class="location"]/text()').extract_first()
            location_2 = response.xpath('//a[@class="location-more"]/text()').extract_first(default='')
            location = location_1 + location_2
            
            
        # -------------------------------------------------------------------------------------------- SALARY
            salary = None   
            
            if(len(data_scrap)) == 2:
                temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold text-gray"]/text()').extract_first()
                salary = temp_salary_1
                if(salary != 'Gaji Dirahasiakan'):
                    temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold currency text-success"]/text()').extract_first()
                    temp_salary_2 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold"][1]/text()').extract_first()
                    temp_salary_3 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold"][2]/text()').extract_first()
                    salary      =temp_salary_1 + ' ' + temp_salary_2.strip() + ' - ' + temp_salary_3.strip()
                  
            elif(len(data_scrap)) == 3:
                temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold text-gray"]/text()').extract_first()
                salary = temp_salary_1
                if(salary != 'Gaji Dirahasiakan'):
                    temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold currency text-success"]/text()').extract_first()
                    temp_salary_2 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold"][1]/text()').extract_first()
                    temp_salary_3 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold"][2]/text()').extract_first()
                    salary      =temp_salary_1 + ' ' + temp_salary_2.strip() + ' - ' + temp_salary_3.strip()
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION LEVEL
            qualification_level = None
        
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
