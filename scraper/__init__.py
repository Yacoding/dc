# -*- coding: utf-8 -*-
import re
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
			self.command += " -a start_urls=" + self.init_start_url( start_urls )	


	def run(self):

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


def get_start_urls(source, tasks):

	BASE_TM_LIST_URL = "http://list.tmall.com/search_product.htm?"
	start_urls = []
	if source.upper() == 'TM':
		regexQ = re.compile('[\?&]q=([^&]+)')
		regex = re.compile('cat=(\d+)')
		for t in tasks:
			resultQ = regexQ.search( t['start_url'] )
			# has q attribute
			if resultQ:
				t['start_url'] = BASE_TM_LIST_URL + 'q=' + resultQ.group(1)
				start_urls.append( ('', t['start_url']) )
			# without q attribute
			else:
				result = regex.search( t['start_url'] )
				if result:
					t['start_url'] = BASE_TM_LIST_URL + 'cat=' + result.group(1)
					start_urls.append( (t['category'], t['start_url']) )

	elif source.upper() == 'JD':
		pass

	return start_urls