import scrapy
from collections import OrderedDict


class YelpSpider(scrapy.Spider):
    
    name = "yelp"
    
    unique_data = set()

    def start_requests(self):

        start_urls = []

        urls = ["https://www.yelp.com/search?find_desc=Restaurants&find_loc=Madison%%2C%%20WI&ns=1&sortby=rating&start=%s",
                "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Atlanta%%2C%%20GA&sortby=rating&start=%s",
                "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Phoenix%%2C%%20AZ&sortby=rating&start=%s",
                "https://www.yelp.com/search?find_desc=Restaurants&find_loc=Minneapolis%%2C%%20MN&sortby=rating&start=%s",
                ]

        for url in urls:
            for i in range(0, 120):
                start_urls.append(url % (i*30))

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        contents = response.selector.xpath(
            '//*[@class="lemon--div__373c0__1mboc u-padding-t3 u-padding-b3 border--top__373c0__19Owr border-color--default__373c0__2oFDT"]')

        for content in contents:
            name = content.css('a.link__373c0__29943::text').extract_first()
            contact = content.css('div.container__373c0__19wDx')
            phone = contact.css('div::text').extract_first()
            if phone is not None and "(" not in phone and len(phone) != 14 :
                phone = ''
            address = contact.css('address>div>span::text').extract_first()
            categories = content.css('div.priceCategory__373c0__3zW0R')

            details = categories.css('span')
            price = len(details[0].css('span::text').extract())
            cuisine = details[1].css('span>span>span>a::text').extract()
            cuisineAll = ''.join(str(elem + ",") for elem in cuisine)
            cuisineAll = cuisineAll[:-1]
            
            uniquename = ""
            if name is not None:
                if address is not None:
                    uniquename = name + address

            result = OrderedDict()
            result['Name'] = name
            result['PhoneNumber'] = phone
            result['Address'] = address
            result['CostRange'] = price
            result['Cuisine'] = cuisineAll


            if uniquename and (uniquename not in self.unique_data):
                self.unique_data.add(uniquename)
                yield result
