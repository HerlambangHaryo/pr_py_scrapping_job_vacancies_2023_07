# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector


class JobsidpagesearchSpider(scrapy.Spider):
    name                 = 'jobsidpage'
    allowed_domains      = ['jobs.id']
    #start_urls           = ['https://www.jobs.id/lowongan/MjY4MDYz/financial-services-consultant-rifan-financindo-bandung-pt?qt_ref=search&qt_page=37&qt_pos=1']
    #start_urls           = ['https://www.jobs.id/lowongan/Mjg4MDg5/operator-manufactur?qt_ref=search&qt_page=1&qt_pos=11']    
    #start_urls           = ['https://www.jobs.id/lowongan/MTc0NzU3/micetour-bet-obaja-international-pt?qt_ref=search&qt_page=1&qt_pos=2']
    
    start_urls           = ['https://www.jobs.id/lowongan/MjkxMTU5/resepsionis-audy-dental-kemang-audy-mandiri-indonesia-pt?qt_ref=search&qt_page=3&qt_pos=1']
    
    
    
    def parse(self, response):    
        # -------------------------------------------------------------------------------------------- INITIALIZE        
            TAG_RE = re.compile(r'<[^>]+>')
            data_scrap_12_6_4       = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"]') 
            
        # -------------------------------------------------------------------------------------------- SOURCE
            source = 'jobs.id'            
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//div[@class="col-sm-10 col-xs-12"]/h5/a/strong[@class="text-muted"]/text()').extract_first(default = None) 
                       
            address = response.xpath('//div[@class="panel panel-default company-profile"]/div[@class="panel-body"]/p[2]/b/text()').extract_first()
            
            location_1 = response.xpath('//span[@class="location"]/text()').extract_first()
            location_2 = response.xpath('//a[@class="location-more"]/text()').extract_first(default='')
            city = location_1 + location_2
            
            phone = None
            website = None
            
            industry = response.xpath('//div[@class="panel panel-default company-profile"]/div[@class="panel-body"]/p[1]/span/a/text()').extract_first()
            
        # -------------------------------------------------------------------------------------------- Job
            
            temp_job_tittle = response.xpath('//h1[@class="clear-top bold"]/text()').extract_first()
            tittle      = temp_job_tittle.strip() 
            
            position = None
            
            salary = None             
            if(len(data_scrap_12_6_4)) == 2:                
                domain = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][1]/h4/a/text()').extract_first()            
                temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold text-gray"]/text()').extract_first()
                salary = temp_salary_1
                if(salary != 'Gaji Dirahasiakan'):
                    temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold currency text-success"]/text()').extract_first()
                    temp_salary_2 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold"][1]/text()').extract_first()
                    temp_salary_3 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/span[@class="semi-bold"][2]/text()').extract_first()
                    salary      =temp_salary_1 + ' ' + temp_salary_2.strip() + ' - ' + temp_salary_3.strip()
                  
            elif(len(data_scrap_12_6_4)) == 3:
                domain = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][2]/h4/a/text()').extract_first()                
                temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold text-gray"]/text()').extract_first()
                salary = temp_salary_1
                if(salary != 'Gaji Dirahasiakan'):
                    temp_salary_1 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold currency text-success"]/text()').extract_first()
                    temp_salary_2 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold"][1]/text()').extract_first()
                    temp_salary_3 = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][3]/h4/span[@class="semi-bold"][2]/text()').extract_first()
                    salary      =temp_salary_1 + ' ' + temp_salary_2.strip() + ' - ' + temp_salary_3.strip()
                    
            placement = None
            employment_type = None
                    
        # -------------------------------------------------------------------------------------------- Requirements
            temp_requirement = response.xpath('//div[@class="job_req"]').extract_first(default='')
            requirement =  TAG_RE.sub('', temp_requirement)
            
            degree = None
            major = None
            gpa = None
            
            experience = None
            if(len(data_scrap_12_6_4)) == 3:
                temp_experience = response.xpath('//div[@class="col-xs-12 col-sm-6 col-md-4"][1]/h4/span[@class="semi-bold"]/text()').extract_first()
                experience      = temp_experience.strip() 
                
            hardskill = None
            softskill = None
            max_age = None
            gender = None
            
        # -------------------------------------------------------------------------------------------- Description
            temp_description = response.xpath('//div[@class="job_desc"]').extract_first(default='')
            description =  TAG_RE.sub('', temp_description)

            jobdesk = None
            benefit = None
            
        # -------------------------------------------------------------------------------------------- Open Closed
            open = response.xpath('//div[@class="col-xs-6"][1]/p/text()').extract_first().replace("Diiklankan sejak", "").strip() 
            closed = response.xpath('//div[@class="col-xs-6"][2]/p/text()').extract_first().replace("Ditutup pada", "").strip() 
            
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

            sql = "INSERT INTO `jobsid`(`source`, `url`, `company`, `address`, `city`, `phone`, `website`, `industry`, `domain`, `tittle`, `position`, `salary`, `placement`, `employment_type`, `requirement`, `degree`, `major`, `gpa`, `experience`, `hardskill`, `softskill`, `max_age`, `gender`, `description`, `jobdesk`, `benefit`, `open`, `closed`, `page`, `terminal`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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