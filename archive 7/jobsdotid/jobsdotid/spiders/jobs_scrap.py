# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class JobssearchSpider(scrapy.Spider):
    name                 = 'jobssearch'
    allowed_domains      = ['jobs.id']
    start_urls           = ['https://www.jobs.id/lowongan-kerja-di-indonesia']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1         
        
        data_scrap       = response.xpath('//div[@class="col-xs-8 col-md-10"]')
        
        for row in data_scrap:                       
            url          = row.xpath('h3/a[@class="bold"]/@href').extract_first()             
            yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
            
        if int(page_number) == 37: 
            page_number = 37
        elif int(page_number) >= 1: 
            page_number = int(page_number) + 1

        next_page     = "https://www.jobs.id/lowongan-kerja?kata-kunci=indonesia&halaman="+ str(page_number)
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
    def parse_page(self, response):
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'jobs.id'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//div[@class="col-sm-10 col-xs-12"]/h5/a/strong[@class="text-muted"]/text()').extract_first(default = None) 
            
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
            
        # -------------------------------------------------------------------------------------------- GROUP PAGE
            page = response.meta.get('page_number')   
        
        
        # -------------------------------------------------------------------------------------------- My SQL
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="karir"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `jobs_new_a`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`, `page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary, qualification_level,page)
            mycursor.execute(sql, val)

            mydb.commit()
        
         # ------------------------------------------------------------------------------- 
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
