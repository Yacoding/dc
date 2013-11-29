# -*- coding: utf-8 -*-
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from myscrapy.spiders.MonitorSpider import MonitorSpider
from scrapy.utils.project import get_project_settings


class CrawlerStarter( object ):

	def __init__(self, spider_name, start_urls=[]):

		if spider_name.upper() == 'MONITORSPIDER':

			self.spider = MonitorSpider( urls_group=start_urls )
			settings = get_project_settings()
			self.crawler = Crawler(settings)
			self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
			self.crawler.configure()
			self.crawler.crawl( self.spider )


	def start(self):

		self.crawler.start()
		log.start()
		# the script will block here until the spider_closed signal was sent
		reactor.run() 
