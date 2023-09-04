# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class UrbanhiresearchSpider(scrapy.Spider):
    name                 = 'urbanhiresearch'
    allowed_domains      = ['urbanhire.com']
    start_urls           = ['https://www.urbanhire.com/jobs?page=1']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1           
        
        data_scrap       = response.xpath('//article[@class= "_1gvQzGfzeaCUVHPZI9QyYM"]')      
        
        for row in data_scrap:                       
            url          = row.xpath('div[@class="row"]/div[@class="col-xs-3 col-sm-3 col-md-3 col-lg-2 "]/div[@class="LzQmZjVcUkFoDVMeHcxKS"]/a/@href').extract_first()
            page_url = 'https://www.urbanhire.com' + url
            yield Request(page_url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
    
        if int(page_number) == 100: 
            page_number = 100
        elif int(page_number) >= 1: 
            page_number = int(page_number) + 1
            
        next_page     = "https://www.urbanhire.com/jobs?page="+ str(page_number)
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
        
       
           
    def parse_page(self, response):
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
            salary_1 = response.xpath('//script/text()').re(".*value.*")
            salary_2 = str(salary_1).split('value')
            salary_3 = salary_2[3].split('",\'')
            salary_4 = salary_3[0].strip('": "')            
            salary = salary_4
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = None  
            
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

            sql = "INSERT INTO `urbanhire`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`, `page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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