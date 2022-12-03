import scrapy
from pydispatch import dispatcher
import json
import time
from scrapy import signals
class HemnetSpider(scrapy.Spider):
    name = "hemnet"
    start_urls = ['https://www.hemnet.se/bostader?housing_form_groups%5B%5D=apartments&location_ids%5B%5D=17755']
    counter = 0
    result = {}

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        for ad in response.css("ul.normal-results > li.normal-results__hit > a::attr(href)"):
            time.sleep(2)
            yield scrapy.Request(url=ad.get(), callback=self.parseurl)
        nextPage = response.css("a.next_page::attr(href)").get()
        if nextPage is not None:
            time.sleep(2)
            response.follow(nextPage, self.parse)
    def parseurl(self, response):
        adress_name = response.css("h1.qa-property-heading::text").get()
        price = response.css("p.property-info__price::text").get()
        price = price.replace("kr","")
        price = price.replace(u"\xa0", "")
        attrdict = {}
        for attr in response.css("div.property-attributes-table > dl.property-attributes-table__area > div.property-attributes-table__row"):
            label = attr.css("dt.property-attributes-table__label::text").get()
            if label is not None :
                label = label.replace(u"\n", "")
                label = label.replace(u"\t", "")
                label = label.strip()
            value = attr.css("dd.property-attributes-table__value::text").get()
            if value is not None :
                value = value.replace(u"\n", "")
                value = value.replace(u"\t", "")
                value = value.strip()
            if label is not None :
                attrdict[label] = value

        self.result[self.counter] = {
            "StreetName": adress_name,
            "price": price,
            "attributes": attrdict
            } 

        self.counter += 1

        
    def spider_closed(self, spider):
            with open('data.json', 'w') as f:
                json.dump(dict, f)


