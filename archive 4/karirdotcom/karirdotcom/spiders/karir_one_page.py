# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request

import datetime
import lxml.html
import re
import mysql.connector


class KarirsearchSpider(scrapy.Spider):
    name                 = 'karirpage'
    allowed_domains      = ['karir.com']
    start_urls           = ['https://www.karir.com/opportunities/1223564']
    
           
    def parse(self, response):
        # ------------------------------------------------------------------------------- URL
            url = response.meta.get('url') 
        
        # ------------------------------------------------------------------------------- SITE
            site = 'karir.com'
        
        # ------------------------------------------------------------------------------- DATE TIME
            now = datetime.datetime.now()        
            date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            
        # ------------------------------------------------------------------------------- DOMAIN OF JOBS
            domain_of_jobs = response.xpath('//li[@class="job--function tooltip__parent"]/text()').extract_first()
            
        # ------------------------------------------------------------------------------- JOB TITLE
            job_title = response.xpath('//h5[@class="title"]/text()').extract_first()
        
        # ------------------------------------------------------------------------------- LOCATION
            location = response.xpath('//li[@class="job--location"]/text()').extract_first()
        
        # ------------------------------------------------------------------------------- EXPERIENCE
            experience = response.xpath('//li[@class="job--experience"]/text()').extract_first()
        
        # ------------------------------------------------------------------------------- SALARY
            salary = response.xpath('//span[@class="salary"]/text()').extract_first()
            
        # ------------------------------------------------------------------------------- SITE
            qualification_1 = response.xpath('//section[@class="b-matte__content"]/ul/li/text()').getall()
        
        
        # ------------------------------------------------------------------------------- SITE
            data_scrap          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()
        
        
        # ------------------------------------------------------------------------------- SITE
            position          = response.xpath('//div[@class="b-stat__footer"]/section[@class="b-stat"]/footer[@class="b-stat__footer"]/text()')[1].extract()
        
        #position          = response.xpath('//div[@class="b-stat__footer"][1]/text()').getall()
        
            if len(data_scrap) == 4:
                qualification_2          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[2]
                qualification_3          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
            
            if len(data_scrap) == 5:
                qualification_2          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[3]
                qualification_3          = response.xpath('//footer[@class="b-stat__footer"]/text()').extract()[4]
        
        
                                                                                                            
                                                                                                            
            qualification_level      = qualification_3 + " " + qualification_2
        
        # ------------------------------------------------------------------------------- MySQL Connector
            mydb = mysql.connector.connect(
              host="localhost",
              user="root",
              passwd="",
              database="paper_one"
            )
        
            mycursor = mydb.cursor()

            sql = "INSERT INTO `karir`(`website`, `url`, `date_time`, `domain_of_the_jobs`, `jobs`, `position`, `experience`, `location`, `salary`, `qualification_level`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
        
