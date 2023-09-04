# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector


class ExecboardinasiapagesearchSpider(scrapy.Spider):
    name                 = 'execboardinasiapage'
    allowed_domains      = ['execboardinasia.com']
    start_urls           = ['https://www.execboardinasia.com/job/legal-senior-manager//']
    
    
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- INITIALIZE        
            TAG_RE = re.compile(r'<[^>]+>')
            
        # -------------------------------------------------------------------------------------------- SOURCE
            source = 'www.execboardinasia.com'            
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = None                 
            address = None        
            city = None            
            phone = None
            website = None   
            industry = response.xpath('//p[@class="jobsummary_ttl"]/text()').extract_first() 
            
        # -------------------------------------------------------------------------------------------- Job
            tittle = response.xpath('//h1[@class="entry-title"]/text()').extract_first()            
            position = None   
            salary = None                
            domain = None                   
            placement = None
            employment_type = None
                    
        # -------------------------------------------------------------------------------------------- Requirements
            requirement =  None            
            degree = None
            major = None
            gpa = None            
            experience = None
            hardskill = None
            softskill = None
            max_age = None
            gender = None
            
        # -------------------------------------------------------------------------------------------- Description
            temp_description = response.xpath('//div[@class="singlejob_desc"]/text()').extract_first(default='hai')   
            description =  TAG_RE.sub('', temp_description)
            
            jobdesk = None
            benefit = None
            
        # -------------------------------------------------------------------------------------------- Open Closed
            open = None 
            closed = None    
            
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

            sql = "INSERT INTO `execboardinasia`(`source`, `url`, `company`, `address`, `city`, `phone`, `website`, `industry`, `domain`, `tittle`, `position`, `salary`, `placement`, `employment_type`, `requirement`, `degree`, `major`, `gpa`, `experience`, `hardskill`, `softskill`, `max_age`, `gender`, `description`, `jobdesk`, `benefit`, `open`, `closed`, `page`, `terminal`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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