# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class JobstreetsearchSpider(scrapy.Spider):
    name                 = 'jobstreetsearch-1000'
    allowed_domains      = ['jobstreet.co.id']
    start_urls           = ['https://www.jobstreet.co.id/en/job-search/job-vacancy/501/?src=16&srcr=16&ojs=1']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 501   
        
        if int(page_number) == 1000: 
            page_number = 1000
        elif int(page_number) >= 501: 
            page_number = int(page_number) + 1
             
        #data_scrap = response.css('title::text').get()
        data_scrap       = response.xpath('//div[@class="position-title header-text"]')
        
        for row in data_scrap:                       
            url          = row.xpath('a[@class="position-title-link"]/@href').extract_first()    
            yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
            
        next_page     = "https://www.jobstreet.co.id/en/job-search/job-vacancy/"+str(page_number)+"/?src=16&srcr=16&ojs=1"     
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number}) 
        
           
    def parse_page(self, response):
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'jobstreet.co.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            temp_company = response.xpath('//div[@class="company_name"]/a/text()').extract_first(default = '')    
            if(temp_company != ''):   
                company = temp_company.strip()
            else:
                temp_company = response.xpath('//div[@class="company_name"]/text()').extract_first(default = None)   
                company = temp_company.strip()  
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h1[@class="job-position"]/text()').extract_first()            
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            temp_experience = response.xpath('//span[@id="years_of_experience"]/text()').extract_first(default = '')  
            if(temp_experience != ''):   
                experience = temp_experience.strip()
            else:
                experience = None 
            
        # -------------------------------------------------------------------------------------------- LOCATION
            temp_location = response.xpath('//span[@class="single_work_location"]/text()').extract_first(default = '') 
            if(temp_location == ''):                
                temp_location = response.xpath('//a[@class="btn btn-link btn-clear clickable"]/text()').extract_first(default = '')
                location = temp_location   
            else:
                location = temp_location.strip()               
            
        # -------------------------------------------------------------------------------------------- SALARY
            salary_1 = response.xpath('//script/text()').re(".*JobAd.Salary.*")
            salary_2 = str(salary_1).split('JobAd.Salary')
            salary_3 = salary_2[1].split('":"')
            salary_4 = salary_3[1].split('"};\']')
            salary = salary_4[0]
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = None      
            
        # -------------------------------------------------------------------------------------------- GROUP PAGE
            page = response.meta.get('page_number')       
         
        # -------------------------------------------------------------------------------------------- MY SQL Connection
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="copy_tesis_one"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `jobstreet_new`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`, `page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary, qualification_level,page)
            mycursor.execute(sql, val)

            mydb.commit()
        
        # -------------------------------------------------------------------------------------------- MY SQL Connection
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
