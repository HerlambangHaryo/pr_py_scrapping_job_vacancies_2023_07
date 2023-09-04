# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector

class JoblikesearchSpider(scrapy.Spider):
    name                 = 'joblikesearch'
    allowed_domains      = ['job-like.com']
    start_urls           = ['https://job-like.com/jobs/?keyword=&order=&page=1']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1   
        
        data_scrap       = response.xpath('//div[@class="col-xs-12"]/a[@class="item-block job "]')
        #data_scrap      = response.xpath('//a[contains(@class, "job")]')
        
        for row in data_scrap:              
            # -------------------------------------------------------------------------------------------- URL
            url          = row.xpath('@href').extract_first()  
            
            # -------------------------------------------------------------------------------------------- SITE
            site         = 'job-like.com'
            
            # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")   
            
            # -------------------------------------------------------------------------------------------- COMPANY
            company      = row.xpath('header/div[@class="hgroup"]/h3[@class="company"]/object/a/text()').extract_first() 
            
            temp_domain_of_jobs = None
            
            data_scrap_2 = row.xpath('footer/object/ul[@class="details cols-4"]/li')
            for rowrow in data_scrap:
                if temp_domain_of_jobs is None:
                    cek_temp_domain_of_jobs = rowrow.xpath('a').getall()
                    if cek_temp_domain_of_jobs:
                        temp_domain_of_jobs = rowrow.xpath('a/text()').getall()
                
            # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = cek_temp_domain_of_jobs
            
            # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = row.xpath('header/div[@class="hgroup"]/h3[@class="title"]/object/a/span/text()').extract_first()   
            
            
                              
            
            # -------------------------------------------------------------------------------------------- POSITION
            position = len(data_scrap_2)
            
            # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
            # -------------------------------------------------------------------------------------------- LOCATION
            location = None
            
            # -------------------------------------------------------------------------------------------- SALARY
            salary = None
            
            # -------------------------------------------------------------------------------------------- QUALIFICATION
            qualification_level = None 
            
            # -------------------------------------------------------------------------------------------- PAGE NUMBER
            
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
                   'page' : page_number}
            