# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from myscrapy.items import ProductItem

import pymongo

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class JDSpider(CrawlSpider):
    name = "jd"
    allowed_domains = ["jd.com"]
    start_urls = []

    rules = (

    	Rule (  SgmlLinkExtractor( allow=(r'item.jd.com'),
                        restrict_xpaths=('//div[@id="plist"]'), 
                        unique=True), 
                callback='parse_item' ),

    	Rule ( SgmlLinkExtractor(  allow=(r'list.jd.com'), 
                        restrict_xpaths=('//div[@class="pagin pagin-m"]//a[@class="next"]'),
                        unique=True), 
                callback='test' ),

    )


    def __init__(self, *args, **kwargs):
        super(JDSpider, self).__init__(*args, **kwargs)
        if kwargs.get('start_url'):
            self.start_urls = [ kwargs.get('start_url') ]


    def parse_item(self, response):
    	sel = Selector(response)
    	item = ProductItem()  
    	item['itemId'] = response.url.split("/")[-1].split(".")[0]
    	item['name'] = sel.xpath('/html/head/title/text()').extract()[0]
        # print dict(item)
        open('file.txt', 'ab').write('1 ' + response.url + '\n')
        return item


    def test(self, response):
    	sel = Selector(response)
    	# print sel.xpath('/html/head/title/text()').extract()[0]
    	open('file.txt', 'ab').write('2 ' + sel.xpath('/html/head/title/text()').extract()[0] + ' ' + response.url + '\n')
