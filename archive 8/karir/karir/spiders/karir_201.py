# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class KarirsearchSpider(scrapy.Spider):
    name                 = 'karir-201'
    allowed_domains      = ['karir.com']
    start_urls           = ['https://www.karir.com/search?q=&sort_order=newest&job_function_ids=&industry_ids=&degree_ids=&major_ids=&location_id=&location=&salary_lower=0&salary_upper=100000000&page=201&grid=list']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 201   
        
        data_scrap       = response.xpath('//div[@class="row opportunity-box"]')
        
        for row in data_scrap:                       
            url          = row.xpath('footer/a[@class="btn --full"]/@href').extract_first()                         
            next_url     = "https://www.karir.com" + url            
            yield Request(next_url, callback=self.parse_page,meta={'url': next_url,'page_number': page_number})
        
        if int(page_number) == 358: 
            page_number = 358
        elif int(page_number) >= 201: 
            page_number = int(page_number) + 1
            
        next_page     = "https://www.karir.com/search?q=&sort_order=newest&job_function_ids=&industry_ids=&degree_ids=&major_ids=&location_id=&location=&salary_lower=0&salary_upper=100000000&page="+ str(page_number) +"&grid=list"   
        
            
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number}) 
        
           
    def parse_page(self, response):
        # -------------------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- SITE
            site = 'karir.com'
            
        # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//a[@class="link"]/text()').extract_first()
            
        # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = response.xpath('//li[@class="job--function tooltip__parent"]/text()').extract_first()
            
        # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h5[@class="title"]/text()').extract_first()         
            
        # -------------------------------------------------------------------------------------------- POSITION
            position          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[1]
            
        # -------------------------------------------------------------------------------------------- EXPERIENCE                
            temp1_experience       = response.xpath('//li[@class="job--experience"]/text()').extract_first()            
            temp2_experience       = re.findall(r'[0-9]+', temp1_experience)
            experience             = temp2_experience[0]
            
        # -------------------------------------------------------------------------------------------- LOCATION
            location = response.xpath('//li[@class="job--location"]/text()').extract_first()              
            
        # -------------------------------------------------------------------------------------------- SALARY 1 & 2  
            temp_salary   = response.xpath('//span[@class="salary"]/text()').extract_first()
            
            salary1 = None
            salary2 = None
            #3.500.000 - 4.500.000
            if(temp_salary != 'Gaji Kompetitif'):
                temp2_salary = temp_salary.split('IDR ')
                temp3_salary = temp2_salary[1].split(' - ')
                salary1      = temp3_salary[0].replace(".", "")
                salary2      = temp3_salary[1].replace(".", "")
            
        # -------------------------------------------------------------------------------------------- QUALIFICATION LEVEL
            qualification_level = None   
            data_scrap          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()
            if len(data_scrap) == 4:
                qualification_level          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[2]
                ql_tambahan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]

            if len(data_scrap) == 5:
                qualification_level          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
                ql_tambahan          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[4]
                
        # -------------------------------------------------------------------------------------------- TYPE OF JOB
            type_of_job = None   
            
        # -------------------------------------------------------------------------------------------- GROUP PAGE
            page = response.meta.get('page_number')   
            
        # -------------------------------------------------------------------------------------------- GROUP PAGE
            group_page = 2   
        
        # -------------------------------------------------------------------------------------------- MY SQL Connection
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="tesis_one_new"
            )            
            mycursor = mydb.cursor()       
                    
        # -------------------------------------------------------------------------------------------- INSERT INTO WEB
            sql = "INSERT INTO `all_website`(`website`, `url`, `date_time`, `company`, `domain_of_the_jobs`, `job_title`, `position`, `experience`, `location`, `salary1`, `salary2`, `qualification_level`, `ql_tambahan`, `type_of_job`, `page`, `group_page`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, company, domain_of_jobs, job_title, position, experience, location, salary1, salary2, qualification_level, ql_tambahan, type_of_job, page, group_page)
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
                   'ql_tambahan' : ql_tambahan, 
                   'type_of_job': type_of_job,
                   'page'       : page, 
                   'group_page' : group_page}
