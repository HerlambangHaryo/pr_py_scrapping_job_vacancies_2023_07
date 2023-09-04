# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector

class IdindeedscrapsearchSpider(scrapy.Spider):
    name                 = 'idindeedscrap'
    allowed_domains      = ['id.indeed.com']
    start_urls           = ['https://id.indeed.com/lowongan-kerja?q=&l=indonesia']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1         
        
        data_scrap       = response.xpath('//h2[@class="title"]')
        
        for row in data_scrap:                       
            temp_url          = row.xpath('a/@href').extract_first()     
            if("/rc/clk?" in temp_url) :
                temp_temp_url = temp_url.replace("/rc/clk?", "")
                url = "https://id.indeed.com/lihat-lowongan-kerja?"+ temp_temp_url
                yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number})
            
        if int(page_number) == 100 :
            page_number = 100
        elif int(page_number) >= 1: 
            page_number = int(page_number) + 1

        next_page     = "https://id.indeed.com/jobs?q=&l=indonesia&start=" + str(page_number) + "0"
        
        yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
           
    def parse_page(self, response):
        # -------------------------------------------------------------------------------------------- INITIALIZE        
            TAG_RE = re.compile(r'<[^>]+>')
            
        # -------------------------------------------------------------------------------------------- SOURCE
            source = 'id.indeed.com'            
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = response.xpath('//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]/text()').extract_first(default='')                    
            address = None      
            city = None            
            phone = None 
            website = None        
            industry = None
            
        # -------------------------------------------------------------------------------------------- Job
            tittle = response.xpath('//h3[@class="icl-u-xs-mb--xs icl-u-xs-mt--none jobsearch-JobInfoHeader-title"]/text()').extract_first()            
            position = None             
            
            domain = None  
            
            temp_data = response.xpath('//span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()').extract() 
            
            salary = None 
            placement = None 
            employment_type = None 
            if(len(temp_data)) > 1:  
                salary = response.xpath('//span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()').extract()[2].strip()  
                placement = response.xpath('//span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()').extract()[0].strip() 
                employment_type = response.xpath('//span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()').extract()[1].strip()                                  
                    
                
                
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
            description =  response.xpath('//div[@class="jobsearch-jobDescriptionText"]').extract_first().strip() 
            
            jobdesk = None
            benefit = None
            
        # -------------------------------------------------------------------------------------------- Open Closed
            open = response.xpath('//div[@class="jobsearch-JobMetadataFooter"]/text()').extract_first(default='').strip() 
            closed = None    
            
        # -------------------------------------------------------------------------------------------- Page & Terminal
            page = response.meta.get('page_number')   
            terminal = 2          
        
        # -------------------------------------------------------------------------------------------- My SQL
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="karir"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `idindeed`(`source`, `url`, `company`, `address`, `city`, `phone`, `website`, `industry`, `domain`, `tittle`, `position`, `salary`, `placement`, `employment_type`, `requirement`, `degree`, `major`, `gpa`, `experience`, `hardskill`, `softskill`, `max_age`, `gender`, `description`, `jobdesk`, `benefit`, `open`, `closed`, `page`, `terminal`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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