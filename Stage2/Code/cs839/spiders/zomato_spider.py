#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:35:22 2019

@author: madanraj
"""

import scrapy

class ZomatoItem(scrapy.Item):
    Name = scrapy.Field()
    Address = scrapy.Field()
    ZipCode = scrapy.Field()
    CostRange = scrapy.Field()
    PhoneNumber = scrapy.Field()
    Cuisine = scrapy.Field()

class ZomatoSpider(scrapy.Spider):
    
    name = "zomato"

    allowed_domains = ['zomato.com']
    
    def start_requests(self):
         start_urls = []
    
         templates = ["https://www.zomato.com/madison-wi/best-restaurants?page=%s",
                      "https://www.zomato.com/atlanta/best-restaurants?page=%s",
                      "https://www.zomato.com/phoenix/best-restaurants?page=%s",
                      "https://www.zomato.com/twin-cities/best-minneapolis-restaurants?page=%s",]
                     
    
         for template in templates:
             for i in range(1,100):
                 start_urls.append(template % (i))
        
         for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    
    def parse(self, response):
        
        contents = response.selector.xpath('//*[@class="card  search-snippet-card     search-card  "]')
        
        
        for content in contents:
            
            title = content.css('.result-title::text').extract_first()
            address = content.css('.search-result-address::text').extract_first()
            if len(address) > 0:
                zipcode = address[-5:]
                if zipcode.isnumeric():
                    address = address[:-6]
                else:
                    zipcode = ""
            cost = len(content.css('.cft_bold'))
            if cost == 0:
                cost = 1
            phoneNumber = content.css('.res-snippet-ph-info::attr(data-phone-no-str)').extract_first()
            if len(phoneNumber) != 14:
                phoneNumber = ""
            cuisinesAll = content.css('.search-page-text>div>span>a::attr(title)').extract()
            cuisine = ''.join(str(elem + ",") for elem in cuisinesAll)
            cuisine = cuisine[:-1]  
        
            result = ZomatoItem()
            result['Name'] = title.strip()
            result['Address'] = address.strip()
            result['ZipCode'] = zipcode
            result['CostRange'] = cost
            result['PhoneNumber'] = phoneNumber.strip()
            result['Cuisine'] = cuisine.strip()
            
           
            yield result
            
            