# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class UrbanhiresearchSpider(scrapy.Spider):
    name                 = 'urbanhirepage'
    allowed_domains      = ['urbanhire.com']
    #start_urls           = ['https://www.urbanhire.com/jobs/system-analyst-pt-elnusa-tbk-rq4t']
    #start_urls           = ['https://www.urbanhire.com/jobs/supervisor-marketing-yamaha-mataram-sakti-dxj']
    #start_urls           = ['https://www.urbanhire.com/jobs/assistant-project-manager-citra-cipta-bika-yiit']
    
    #start_urls           = ['https://www.urbanhire.com/jobs/hrga-spv-pt-surya-sapta-cakrawala-juww']
    start_urls           = ['https://www.urbanhire.com/jobs/account-director-pt-merah-cipta-media-fdu8']
    #start_urls           = ['https://www.urbanhire.com/jobs/center-experience-manager-wall-street-english-indonesia-whra']
    
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'urbanhire.com'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//span[@class="_3ZKIO3XKqd4U0n5jOm_Ucr"]/a/text()').extract_first() 
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = response.xpath('//span[@class="_1TeZcqWyvZFkL8gVFanutx text-u-c"]/a/text()').extract_first()  
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h1[@class="_25NoLfsDQ7ltbJ_l-9uEoA"]/text()').extract_first()            
            
            check = response.xpath('//article[@class="_2oP8NSJqkqgFCV4P6T07RN wWhkHR3jP1-zPKWEv1ECi"]/p')
            
        # -------------------------------------------------------------------------------------------- POSITION
            if(len(check) == 3):
                position = response.xpath('//article[@class="_2oP8NSJqkqgFCV4P6T07RN wWhkHR3jP1-zPKWEv1ECi"]/p[3]/text()').extract_first()
            elif(len(check) == 4):
                position = response.xpath('//article[@class="_2oP8NSJqkqgFCV4P6T07RN wWhkHR3jP1-zPKWEv1ECi"]/p[4]/text()').extract_first()        
        # -------------------------------------------------------------------------------------------- EXPERIENCE            
            if(len(check) == 3):
                experience = response.xpath('//article[@class="_2oP8NSJqkqgFCV4P6T07RN wWhkHR3jP1-zPKWEv1ECi"]/p[3]/text()').extract_first()
            elif(len(check) == 4):
                experience = response.xpath('//article[@class="_2oP8NSJqkqgFCV4P6T07RN wWhkHR3jP1-zPKWEv1ECi"]/p[4]/text()').extract_first()
            
        # -------------------------------------------------------------------------------------------- LOCATION
            location = response.xpath('//span[@class="ZFi0kbZZx9OLFmFtS0_L7"]/a/text()').extract_first()                
            
        # -------------------------------------------------------------------------------------------- SALARY            
            #salary_1 = response.xpath('//script/text()').re(".*value.*")
            #salary_2 = str(salary_1).split('value')
            #salary_3 = salary_2[3].split('",\'')
            #salary_4 = salary_3[0].strip('": "')       
            
            salary_1 = response.xpath('//script/text()').re(".*value.*")
            #salary_2 = str(salary_1).split('value')
            #salary_3 = salary_2[3].split('",\'')
            #salary_4 = salary_3[0].strip('": "')  
            salary = salary_1
            
            
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
