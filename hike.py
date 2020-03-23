# -*- coding: utf-8 -*-
import scrapy


class HikeSpider(scrapy.Spider):
    name = 'hike'
    allowed_domains = ['www.nynjtc.org']
    start_urls = ['https://www.nynjtc.org/view/hike_ny']

    def parse(self, response):
        hikes = response.xpath("//table[@class='views-table sticky-enabled cols-8 table table-hover table-striped']/tbody/tr")
        for hike in hikes:
            name = hike.xpath(".//td[2]/a/text()").get()
            park = hike.xpath(".//td[3]/text()").get()
            length = hike.xpath(".//td[5]/text()").get()
            link = hike.xpath(".//td[2]/a/@href").get()
            difficulty = hike.xpath(".//td[6]/text()").get()
            features = hike.xpath(".//td[7]/text()").get()

            yield response.follow(url=link,callback=self.parse_hike,meta={'hike_name':name,'length':length,'park':park,'difficulty':difficulty,'features':features})
        

    def parse_hike(self,response):
        name = response.request.meta['hike_name']
        length = response.request.meta['length']
        park = response.request.meta['park']
        difficulty = response.request.meta['difficulty']
        features = response.request.meta['features']
        rows = response.xpath("//span[@class='field-content geo-location-coordinates']")
        for row in rows: 
            geography = row.xpath(".//text()").get()
            yield {
                'park':park,
                'hike':name,
                'geography':geography,
                'length':length,
                'difficulty':difficulty,
                'features':features
            }