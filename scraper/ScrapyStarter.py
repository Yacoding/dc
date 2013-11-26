# -*- coding: utf-8 -*-
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

from django.utils.encoding import smart_str, smart_unicode

import os
from urllib import quote
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class ScrapyStarter( object ):

	def __init__(self):
		self.command = ''


	def create(self, spider_name, action_type="DEF_CALL", start_urls=[]):

		if spider_name.upper() not in ['TM', 'JD', 'TM_CAT']:
			print '[Console]: No spider.'
			return

		self.command = "scrapy crawl " + spider_name.lower() 

		self.command += " -a action_type=" + action_type

		if action_type == "BUSINESS_CALL":
			now = datetime.now().strftime('%Y%m%d_%H-%M-%S')
			self.export_file_name = spider_name.lower() + now
			self.command += " -a export_file_name=" + self.export_file_name

		if len(start_urls) > 0:
			self.command += " -a start_urls=" + self.init_start_url(start_urls)	


	def run(self):

		print self.command
		os.system( self.command )


	def init_start_url(self, start_urls):

		result = ''

		for i in start_urls:
			result += '####' + quote(i[0].encode()) + '____' + i[1]

		return result


	def get_export_file_name(self):

		return self.export_file_name + '.xls' if self.export_file_name else None


	def get_excel_file(self):

		return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'myscrapy', 'download', self.get_export_file_name() )


	def get_file_name_and_content(self):
		"""Get binary string of excel file"""
		excel_file = open(self.get_excel_file(), "rb")
		file_content = excel_file.read()
		excel_file.close()
		return self.get_export_file_name(), file_content