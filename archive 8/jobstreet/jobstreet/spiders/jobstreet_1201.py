# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class JobstreetsearchSpider(scrapy.Spider):
    name                 = 'jobstreet-1201'
    allowed_domains      = ['jobstreet.co.id']
    start_urls           = ['https://www.jobstreet.co.id/en/job-search/job-vacancy/1201/?src=16&srcr=16&ojs=1']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1201   
        
        data_scrap       = response.xpath('//div[@class="position-title header-text"]')
        
        for row in data_scrap:                       
            url          = row.xpath('a[@class="position-title-link"]/@href').extract_first()    
            yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
        
        if int(page_number) == 1400: 
            page_number = 1400
        elif int(page_number) >= 1201: 
            page_number = int(page_number) + 1
            
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
                if (temp_company is not None): 
                    company = temp_company.strip()
                else:
                    company = None
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h1[@class="job-position"]/text()').extract_first()            
            
        # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE
            temp_experience = response.xpath('//span[@id="years_of_experience"]/text()').extract_first(default = '')  
            if(temp_experience != ''):   
                temp2_experience = temp_experience.strip()
                temp3_experience = re.findall(r'[0-9]+', temp2_experience)
                experience       = temp3_experience[0]
            else:
                experience = None 
            
        # -------------------------------------------------------------------------------------------- LOCATION
            temp_location = response.xpath('//span[@class="single_work_location"]/text()').extract_first(default = '') 
            if(temp_location == ''):                
                temp_location = response.xpath('//a[@class="btn btn-link btn-clear clickable"]/text()').extract_first(default = '')
                location = temp_location   
            else:
                location = temp_location.strip()               
            
        # -------------------------------------------------------------------------------------------- SALARY 1 & 2            
            salary_a = response.xpath('//script/text()').re(".*JobAd.Salary.*")
            salary_b = str(salary_a).split('JobAd.Salary')            
            if (len(salary_b) > 1):
                salary_c = salary_b[1].split('":"')
                salary_d = salary_c[1].split('"};\']')
                salary_e = salary_d[0].split('-')
                salary1   = salary_e[0]
                salary2   = salary_e[1]
            else:
                salary1   = None
                salary2   = None
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION LEVEL
            qualification_level = None     
            
        # -------------------------------------------------------------------------------------------- TYPE OF JOB
            type_of_job = None   
            
        # -------------------------------------------------------------------------------------------- GROUP PAGE
            page = response.meta.get('page_number')   
            
        # -------------------------------------------------------------------------------------------- GROUP PAGE
            group_page = 7   
        
        # -------------------------------------------------------------------------------------------- MY SQL Connection
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="tesis_one_new"
            )
            
            mycursor = mydb.cursor()       
                    
        # -------------------------------------------------------------------------------------------- INSERT INTO WEB
            sql = "INSERT INTO `all_website`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `job_title`, `position`, `experience`, `location`, `salary1`, `salary2`, `qualification_level`, `type_of_job`, `page`, `group_page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary1, salary2, qualification_level, type_of_job, page, group_page)
            mycursor.execute(sql, val)
            mydb.commit()
                
        
        # -------------------------------------------------------------------------------------------- MY SQL Connection
            yield {'site': site, 
                   'url' : url, 
                   'date_time' : date_time, 
                   'company'   : company, 
                   'domain_of_jobs' : domain_of_jobs, 
                   'job_title'  : job_title, 
                   'position'   : position, 
                   'experience' : experience, 
                   'location'   : location, 
                   'salary1'    : salary1,  
                   'salary2'    : salary2, 
                   'qualification_level' : qualification_level, 
                   'type_of_job': type_of_job,
                   'page'       : page, 
                   'group_page' : group_page}
