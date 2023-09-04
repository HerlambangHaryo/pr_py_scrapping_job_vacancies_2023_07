# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector


class JoblikepagesearchSpider(scrapy.Spider):
    name                 = 'joblikepage'
    allowed_domains      = ['job-like.com']
    start_urls           = ['https://job-like.com/jobdata/3750717/']
    
    
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- INITIALIZE        
            TAG_RE = re.compile(r'<[^>]+>')
            
        # -------------------------------------------------------------------------------------------- SOURCE
            source = 'job-like.com'            
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//div[@class="header-detail"]/div[@class="hgroup"]/div[@class="block"]/h3/a/text()').extract_first()                  
            address = response.xpath('//div[@class="company-about"]/div[@class="item address"]/div[@class="body"]/div[@class="value"]/text()').extract_first().strip()       
            
            city1 = response.xpath('//div[@class="company-about"]/div[@class="item area"]/div[@class="body"]/div[@class="value"]/span/a[1]/text()').extract_first(default='')              
            city2 = response.xpath('//div[@class="company-about"]/div[@class="item area"]/div[@class="body"]/div[@class="value"]/span/a[2]/text()').extract_first(default='')  
            city =city1 + ' ' + city2
            
            phone = response.xpath('//div[@class="company-about"]/div[@class="item phone_number"]/div[@class="body"]/div[@class="value"]/text()').extract_first() 
            website = response.xpath('//div[@class="company-about"]/div[@class="item website"]/div[@class="body"]/div[@class="value"]/a/text()').extract_first()        
            industry = response.xpath('//div[@class="company-about"]/div[@class="item industry"]/div[@class="body"]/div[@class="value"]/text()').extract_first() 
            
        # -------------------------------------------------------------------------------------------- Job
            tittle = response.xpath('//div[@class="header-detail"]/div[@class="hgroup"]/div[@class="block"]/h1/text()').extract_first()             
            position = None   
            
            temp_salary_domain = response.xpath('//ul[@class="details cols-3 no-margin-top"]').extract_first(default='')
            salary = TAG_RE.sub(' # ', temp_salary_domain)                 
            domain = TAG_RE.sub(' # ', temp_salary_domain)                    
            placement = None
            employment_type = None
                    
        # -------------------------------------------------------------------------------------------- Requirements
            temp_requirement_description = response.xpath('//article[@class="lead"]').extract_first(default='')
            requirement =  TAG_RE.sub('', temp_requirement_description)
            
            degree = None
            major = None
            gpa = None            
            experience = None
            hardskill = None
            softskill = None
            max_age = None
            gender = None
            
        # -------------------------------------------------------------------------------------------- Description
            description =  TAG_RE.sub('', temp_requirement_description)
            
            jobdesk = None
            benefit = None
            
        # -------------------------------------------------------------------------------------------- Open Closed
            open = response.xpath('//ul[@class="details cols-3 no-margin-bottom"]/li[1]/text()').extract_first().strip()  
            closed = response.xpath('//ul[@class="details cols-3 no-margin-bottom"]/li[2]/text()').extract_first().strip()    
            
        # -------------------------------------------------------------------------------------------- Page & Terminal
            page = response.meta.get('page_number')   
            terminal = 1          
        
        # -------------------------------------------------------------------------------------------- My SQL
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="karir"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `joblike`(`source`, `url`, `company`, `address`, `city`, `phone`, `website`, `industry`, `domain`, `tittle`, `position`, `salary`, `placement`, `employment_type`, `requirement`, `degree`, `major`, `gpa`, `experience`, `hardskill`, `softskill`, `max_age`, `gender`, `description`, `jobdesk`, `benefit`, `open`, `closed`, `page`, `terminal`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (source, url, company, address, city, phone, website, industry, domain, tittle, position, salary, placement, employment_type, requirement, degree, major, gpa, experience, hardskill, softskill, max_age, gender, description, jobdesk, benefit, open, closed, page, terminal)
            mycursor.execute(sql, val)

            mydb.commit()
            
         # ------------------------------------------------------------------------------- 
            yield {'source': source, 
                   'url': url, 
                   
                   'company' : company, 
                   'address' : address, 
                   'city' : city, 
                   'phone' : phone, 
                   'website' : website, 
                   'industry' : industry, 
                   
                   'domain' : domain, 
                   'tittle' : tittle, 
                   'position' : position, 
                   'salary' : salary, 
                   'placement' : placement, 
                   'employment_type' : employment_type, 
                                      
                   'requirement' : requirement,                    
                   'degree' : degree,                    
                   'major' : major,                    
                   'gpa' : gpa,                    
                   'experience' : experience, 
                   'hardskill' : hardskill, 
                   'softskill' : softskill,
                   'max_age' : max_age,
                   'gender' : gender,
                   
                   'description' : description,
                   'jobdesk' : jobdesk,
                   'benefit' : benefit,
                   
                   'open' : open,
                   'closed' : closed,
                   
                   'page' : page, 
                   'terminal' : terminal
                  }