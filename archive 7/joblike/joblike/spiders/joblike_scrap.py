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
        
        data_scrap       = response.xpath('//div[@class="col-xs-12"]')
        #data_scrap      = response.xpath('//a[contains(@class, "job")]')
        
        for row in data_scrap:              
            # -------------------------------------------------------------------------------------------- URL
            url          = row.xpath('//a[contains(@class, "job")]/@href').extract_first()  
            
            # -------------------------------------------------------------------------------------------- SITE
            site         = 'job-like.com'
            
            # -------------------------------------------------------------------------------------------- DATE TIME            
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")   
            
            # -------------------------------------------------------------------------------------------- COMPANY
            company      = row.xpath('//a[contains(@class, "job")]/header/div[@class="hgroup"]/h3[@class="company"]/object/a/text()').extract_first() 
            
            # -------------------------------------------------------------------------------------------- DOMAIN of the JOBS
            domain_of_jobs = None
            
            # -------------------------------------------------------------------------------------------- JOB TITLE
            job_title = row.xpath('//a[contains(@class, "job")]/header/div[@class="hgroup"]/h3[@class="title"]/object/a/span/text()').extract_first()   
            
            data_scrap_2 = row.xpath('//a[contains(@class, "job")]/footer/object/ul[@class="details cols-4"]/li')
            salary = None
            
            
                    
            
            # -------------------------------------------------------------------------------------------- EXPERIENCE
            experience = None
            
            
            yield{'site': site, 
                   'url': url, 
                   'date_time' : date_time,
                   'company': company, 
                   'domain_of_jobs': domain_of_jobs, 
                   'job_title' : job_title, 
                   'salary' : salary}