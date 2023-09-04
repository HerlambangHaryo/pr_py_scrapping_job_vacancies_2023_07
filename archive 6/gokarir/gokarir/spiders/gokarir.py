# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class GokarirsearchSpider(scrapy.Spider):
    name                 = 'gokarir'
    allowed_domains      = ['gokarir.com']
    start_urls           = ['https://gokarir.com/jobs?p=8']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 8   
        
        data_scrap       = response.xpath('//li[contains(@class, " ")]')
        
        for row in data_scrap:              
            # -------------------------------------------------------------------------------------------- URL
            url          = row.xpath('div[@class="desktop-listing-content"]/div[@class="noMP col-md-7 col-sm-7 col-xs-7"][1]/a[1]/@href').extract_first()   
            
            # -------------------------------------------------------------------------------------------- SITE
            site = 'gokarir.com'
            
            # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")   
            
            # -------------------------------------------------------------------------------------------- COMPANY
            company = row.xpath('//div[@class="listing-info"]/span[@class="opaque"][1]/text()').extract_first() 
            
            # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
            # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = row.xpath('div[@class="desktop-listing-content"]/div[@class="noMP col-md-7 col-sm-7 col-xs-7"][1]/a[2]/div[@class="listing-title"]/text()').extract_first().strip()   
            
            # -------------------------------------------------------------------------------------------- POSITION
            position = None
            
            # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
            # -------------------------------------------------------------------------------------------- LOCATION
            location = row.xpath('//div[@class="listing-info"]/span[@class="opaque"][2]/text()').extract_first()             
            
            # -------------------------------------------------------------------------------------------- SALARY
            salary1 = None
            salary2 = None
            salary = row.xpath('div[@class="desktop-listing-content"]/div[@class="noMP col-md-5 col-sm-5 col-xs-5"][1]/div[@class="listing-type"]/span[@class="list-salary"]/text()').extract_first()
            
            if(salary is not None):
                if ('Gaji' in salary):
                    salary = None
                elif ('Dirahasiakan' in salary):
                    salary = None
                elif ('DIBICARAKAN' in salary):
                    salary = None
                elif ('Nego' in salary):
                    salary = None                    
                else :                   
                    salary = salary
                    salary = salary.replace(",", "")
                    salary = re.findall(r'[0-9]+', salary)
                    
                    if(len(salary) > 1):
                        salary1 = int(''.join(str(i) for i in intsalary[0]))
                        salary2 = int(''.join(str(i) for i in intsalary[1]))
                    else:
                        salary1 = salary
                        salary2 = None


            # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = None 
            
            # -------------------------------------------------------------------------------------------- TYPE OF JOB
            type_of_job = None 
            
            # -------------------------------------------------------------------------------------------- GROUP PAGE
            page = response.meta.get('page_number') 
            
            # -------------------------------------------------------------------------------------------- GROUP PAGE
            group_page = 1  
            
            # -------------------------------------------------------------------------------------------- MY SQL Connection
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="tesis_one_testing"
            )
            
            mycursor = mydb.cursor() 
            
            # -------------------------------------------------------------------------------------------- INSERT INTO WEB
            sql = "INSERT INTO `testing`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `job_title`, `position`, `experience`, `location`, `salary1`, `salary2`, `qualification_level`, `type_of_job`, `page`, `group_page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary1, salary2, qualification_level, type_of_job, page, group_page)
            mycursor.execute(sql, val)
            mydb.commit()
            
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
            
        if int(page_number) == 10: 
            page_number = 10
        elif int(page_number) >= 1: 
            page_number = int(page_number) + 1            
        
        next_page     = "https://gokarir.com/jobs?p=" + str(page_number)     
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
 