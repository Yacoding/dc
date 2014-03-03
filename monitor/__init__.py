# -*- coding: utf-8 -*-
import os
import re
import xlrd
from datetime import datetime


class MonitorTemplateHandler(object):

	upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload')


	def __init__(self, t_file):
		"""
		Parameters
    	----------
    	t_file : FileUpload instance
		"""
		date = datetime.now()
		now = date.strftime('%Y%m%d_%H-%M-%S')
		self.today = date.strftime('%Y-%m-%d')

		self.xls_file = os.path.join( self.upload_path, now + t_file.name )
		self._save( t_file.read() )


	def _save(self, t_stream):

		with open( self.xls_file, 'wb+' ) as xls:
			xls.write( t_stream )


	def _remove(self):

		try:
			os.remove( self.xls_file )
		except:
			return


	def explain(self):

		wb = xlrd.open_workbook( self.xls_file )
		table = wb.sheet_by_index(0)
		tasks = []

		if table.nrows > 1 and table.ncols > 0:
			for row in range(1, table.nrows):
				task = self._read_task( table, row )
				if task: tasks.append( task )

		self._remove()
		return tasks


	def _read_task(self, table, row):

		values = table.row_values(row)
		sku = values[0]
		if not sku:
			return

		def tmall_main(url):
			result = re.compile('[\?&]id=(\d+)').search(url)
			if result:
				base_url = url.split('item.htm?')[0]
				task['urls'].append( '%sitem.htm?id=%s' % (base_url, result.group(1)) )

		def tmall_assist(url):
			if url.find('list.tmall.com') > -1:
				result = re.compile('[\?&]q=([^&]+)').search(url)
				if result:
					task['extras'].append( 'http://list.tmall.com/search_product.htm?q=%s' % result.group(1) )
			elif url.find('detail.tmall.com') > -1:
				result = re.compile('[\?&]id=(\d+)').search(url)
				if result:
					task['extras'].append( 'http://detail.tmall.com/item.htm?id=%s' % result.group(1) )

		def others(urls):
			for url in urls:
				if url:
					if url.find('item.yixun.com') > -1 or url.find('http://item.yhd.com/') > -1:
						task['urls'].append( url.split('?')[0] )
					else:
						task['urls'].append( url )

		task = { 'sku': sku, 'date': self.today, 'state': 1, 'urls': [], 'extras': [] }

		if len(values) > 2 and values[1]:
			# handle tmall's main link
			tmall_main( values[1] )

		if len(values) > 3 and values[2]:
			# handle tmall's assist link
			tmall_assist( values[2] )

		if len(values) > 4:
			# handle others' links
			others( values[3:] )

		task['urls'].append( "http://item.feifei.com/%s.html" % sku )
		return task


def save_tasks_to_mongo(collection, tasks):

	for task in tasks:
		if collection.find_one( {'sku': task['sku']} ):
			collection.remove( {'sku': task['sku']} )
		collection.insert( task )