# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from myscrapy.items import TmCatItem

from datetime import date

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class TMCatSpider(BaseSpider):

    name = "tm_cat"
    allowed_domains = ["tmall.com", "taobao.com"]
    start_urls = [
        "http://www.tmall.com/go/rgn/mfp2012/all-cat-asyn.php",
    ]


    def parse(self, response):
        """ Main parse function
        """
    	sel = Selector(response)
    	item = TmCatItem() 

        item['cat'] = {}

        first_level_node = sel.xpath('//li[@class="subItem"]')

        for node in first_level_node:
            first_level_title = node.xpath('.//h3[@class="subItem-hd"]/a/text()').extract()[0]
            second_level_node = node.xpath('.//p[@class="subItem-cat"]/a')

            second_level = []

            for i in second_level_node:
                second_level_title = i.xpath('./text()').extract()[0]
                second_level_link = i.xpath('./@href').extract()[0]
                second_level.append( (second_level_title, second_level_link) )

            item['cat'][first_level_title] = dict( second_level )

        return item
