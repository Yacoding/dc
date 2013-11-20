# -*- coding: utf8 -*-
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

import os


class ScrapyStarter( object ):

	def __init__(self):
		self.command = ''


	def create(self, spider_name, start_url=''):

		if spider_name.upper() not in ['TM', 'JD', 'TM_CAT']:
			print '[Console]: No spider.'
			return

		self.command = "scrapy crawl " + spider_name.lower() 

		if start_url:
			self.command += " -a start_url=" + start_url


	def run(self):

		os.system( self.command )