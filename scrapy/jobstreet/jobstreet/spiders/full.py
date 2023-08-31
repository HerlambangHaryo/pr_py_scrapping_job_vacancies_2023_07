# -*- coding: utf-8 -*-
from calendar import c
import scrapy
from scrapy.spiders import CrawlSpider, Rule, Request


import datetime
import lxml.html
import re
import mysql.connector 
import json 

class JobstreetsearchSpider(scrapy.Spider):
    name                 = 'full'
    allowed_domains      = ['jobstreet.co.id'] 
    start_urls           = ['https://www.jobstreet.co.id/id/jobs?pg=1'] 
    #  https://www.jobstreet.co.id/id/jobs?pg=1
    
    def parse(self, response):    
        page_number = response.meta.get('page_number') or 1         
        
        bodyx = response.xpath('//script[2]').extract_first()  
        bodysplit = bodyx.split('"jobUrl":"')
        stringcount = len(bodysplit)         
        counter = 1
        
        yield {'stringcount': stringcount}
        
        for row in bodysplit:   
            if(counter < stringcount):
                prelink = bodysplit[counter]
                prelink2 = prelink.split('","jobTitleSlug":"')[0]
                url = prelink2.replace('\\u002F', '/')   
                 
                yield Request(url, callback=self.parse_page,meta={'url': url,'page_number': page_number}) 
                counter+=1
            else:
                break
                
        if int(page_number) == 1600 :
            page_number = 1600 
        elif int(page_number) >= 1 :
            page_number = int(page_number) + 1
            next_page     = "https://www.jobstreet.co.id/id/jobs?pg=" + str(page_number)
            yield Request(next_page, callback=self.parse,meta={'page_number': page_number})
            
    def parse_page(self, response):    
        
        # ----------------------------------------------------------------------------------   
            url = response.meta.get('url') 
            url_str = str(url.replace("'", "\\'"))
        # ---------------------------------------------------------------------------------- 
            scriptx = response.xpath('//script[2]/text()').extract_first() 
            scriptx_str = str(scriptx.replace("'", "\\'"))
        # ----------------------------------------------------------------------------------  
            host="localhost"
            user="root" 
            database="pr_scraping_job_vacancy_indonesia_2023_07"
            mydb = mysql.connector.connect(host=host,user=user,password="",database=database)
            mycursor = mydb.cursor()
        # ----------------------------------------------------------------------------------  
            query_commit = "select "
            # ----------------------------------------------    
            query_commit += " *  " 
            query_commit += " from `jobstreet_raws_2023_07` " 
            query_commit += " WHERE `url` like '"+url_str+"' "
            # ----------------------------------------------      
            mycursor.execute(query_commit)
            result =  mycursor.fetchall()
            # ----------------------------------------------  
            total_rows = len(result)   
            # ----------------------------------------------  
            if(total_rows == 0):  
                # ------------------------------------------ 
                status = "Inserted"
                # ------------------------------------------ 
                query_commit = "INSERT INTO `jobstreet_raws_2023_07`( "
                # ------------------------------------------   
                query_commit += " `url`, " 
                query_commit += " `scriptx` " 
                query_commit += " ) VALUES ( "
                # ------------------------------------------    
                query_commit += " '" + url_str + "', "  
                query_commit += " '" + scriptx_str + "' "  
                query_commit += " ) "
                # ------------------------------------------  
                mycursor.execute(query_commit)
                mydb.commit()   
            # ----------------------------------------------  
            elif(total_rows > 0):  
                # ------------------------------------------ 
                status = "Duplicated"
            # ----------------------------------------------  
        # ---------------------------------------------------------------------------------- 
            yield {'url': url, 'status': status }
        # ---------------------------------------------------------------------------------- 