# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import mysql.connector

class IddotindeedsearchSpider(scrapy.Spider):
    name                 = 'iddotindeedsearch'
    allowed_domains      = ['id.indeed.com']
    start_urls           = ['https://id.indeed.com/lowongan-kerja-di-indonesia']
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1   
        
        # ------------------------------------------------------------------------------- SITE 
        site = 'id.indeed.com'
            
        # ------------------------------------------------------------------------------- DATE TIME 
        now = datetime.datetime.now()        
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # ------------------------------------------------------------------------------- DOMAIN OF THE JOBS
        domain_of_jobs = None
            
        # ------------------------------------------------------------------------------- POSITION
        position = None
            
        # ------------------------------------------------------------------------------- EXPERIENCE
        experience = None
            
        # ------------------------------------------------------------------------------- QUALIFICATION LEVEL
        qualification_level = None
            
        # ------------------------------------------------------------------------------- 
        data_scrap       = response.xpath('//div[contains(@class, "jobsearch-SerpJobCard")]')
        
        
        for row in data_scrap: 
            # ------------------------------------------------------------------------------- URL
            url          = row.xpath('a[contains(@class, "jobtitle")]/@href').extract_first() 
            #temp_job_title    = row.xpath('div[@class="sjcl"]/div/span[@class="company"]/text()').extract_first(default='')
            temp_job_title    = row.xpath('a[contains(@class, "jobtitle")]/text()').extract_first(default='')
            job_title    = temp_job_title.strip()
            location     = row.xpath('div[@class="sjcl"]/div[@class="location"]/text()').extract_first() 
            salary       = row.xpath('div[@class="paddedSummary"]/table/tbody/tr/td[@class="snip"]/div[@class="salarySnippet"]/span[@class="salary no-wrap"]/text()').extract_first() 
               
        # ------------------------------------------------------------------------------- MYSQL 
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="paper_one"
            )

            mycursor = mydb.cursor()

            sql = "INSERT INTO `indeed`(`website`, `url`, `date_time`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (site, url, date_time, domain_of_jobs, job_title, position, experience, location, salary, qualification_level)
            mycursor.execute(sql, val)

            mydb.commit()

        # ------------------------------------------------------------------------------- 
            yield {'site': site, 
               'url': url, 
               'date_time' : date_time, 
               'domain_of_jobs' : domain_of_jobs, 
               'job_title' : job_title, 
               'position' : position, 
               'experience' : experience, 
               'location' : location, 
               'salary' : salary, 
               'qualification_level' : qualification_level}
           
   