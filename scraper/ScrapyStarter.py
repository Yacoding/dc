# -*- coding: utf8 -*-
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

import os


class ScrapyStarter( object ):

	def __init__(self):
		self.command = ''


	def create(self, spider_name, start_urls=[]):

		if spider_name.upper() not in ['TM', 'JD', 'TM_CAT']:
			print '[Console]: No spider.'
			return

		self.command = "scrapy crawl " + spider_name.lower() 

		if len(start_urls) > 0:
			print start_urls
			# self.command += " -a start_urls=" + start_urls
			self.command += " -a start_urls=" + self.init_start_url(start_urls)
			print self.command


	def run(self):

		os.system( self.command )


	def init_start_url(self, start_urls):

		result = ''

		for i in start_urls:
			result += i[0] + '____' + i[1] + '####'

		return result