# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector
import json
from pprint import pprint

import urllib.request
from bs4 import BeautifulSoup, Comment


class urbanhirepagesearchSpider(scrapy.Spider):
    name                 = 'urbanhirepage'
    allowed_domains      = ['urbanhire.com']
    start_urls           = ['https://www.urbanhire.com/jobs/content-quality-specialist-indojasa-andalan-global-50zc']
    
    
    def parse(self, response): 
        # -------------------------------------------------------------------------------------------- INITIALIZE
            page = urllib.request.urlopen("https://www.urbanhire.com/jobs/content-quality-specialist-indojasa-andalan-global-50zc")
            content = page.read().decode('utf-8')
            soup = BeautifulSoup(content, 'html.parser')
            comments = soup.findAll(text=lambda text:isinstance(text, Comment))
            [comment.extract() for comment in comments]
            tittle = soup.find("h1", {"data-reactid": "97"}).text
        # -------------------------------------------------------------------------------------------- INITIALIZE        
            TAG_RE = re.compile(r'<[^>]+>')
            
        # -------------------------------------------------------------------------------------------- SOURCE
            source = 'urbanhire.com'            
            url = response.meta.get('url') 
            
        # -------------------------------------------------------------------------------------------- COMPANY
            company = None                   
            address = None      
            city = None            
            phone = None 
            website = None        
            industry = None
            # <h1 class="_25NoLfsDQ7ltbJ_l-9uEoA" data-reactid="97">Content Quality Specialist</h1>
            #response.css('span[property="city"]::text').extract_first() 
            #tittle = response.xpath('//h1[data-reactid="97"]/text()').extract_first(default='')         
            #contains(text(),'telephone'
        # -------------------------------------------------------------------------------------------- Job
            #tittle = response.xpath('//h1[@data-reactid="97"]/text()').extract()     
            
            position = None  
            domain = None              
            salary = None 
            placement = None 
            employment_type = None 
            placement = None  
                
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
            description =  None 
            
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

            sql = "INSERT INTO `urbanhire`(`source`, `url`, `company`, `address`, `city`, `phone`, `website`, `industry`, `domain`, `tittle`, `position`, `salary`, `placement`, `employment_type`, `requirement`, `degree`, `major`, `gpa`, `experience`, `hardskill`, `softskill`, `max_age`, `gender`, `description`, `jobdesk`, `benefit`, `open`, `closed`, `page`, `terminal`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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