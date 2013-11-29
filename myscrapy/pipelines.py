# -*- coding: utf-8 -*-

import os
import sys
import pymongo
from datetime import datetime
from myscrapy.export import ExportExcelEveryItem
from scrapy.contrib.exporter import JsonItemExporter, JsonLinesItemExporter


class PrintPipeline(object):

	def process_item(self, item, spider):
		return item
		


class TutorialPipeline(object):

	def open_spider(self, spider):
		print "[open] " + spider.name
		return

	def process_item(self, item, spider):
		return item

	def close_spider(self, spider):
		print "[close] " + spider.name


class MongoPipeline(object):

	def __init__(self):
		self.conn = pymongo.Connection('127.0.0.1', 27017)

	def process_item(self, item, spider):
		self.conn['test']['tm'].save(dict(item))
		return item


class JsonItemPipeline(object):

	def open_spider(self, spider):
		self.file = open('test.json', 'w+b')
		self.exporter = JsonItemExporter(self.file)
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item	


class JsonLinesItemPipeline(object):

	def open_spider(self, spider):
		self.file = open('test.json', 'w+b')
		self.exporter = JsonLinesItemExporter(self.file)

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item


class MonitorPipeline(object):

	def open_spider(self, spider):
		self.cols = spider.cols
		self.start_urls = spider.start_urls

		self.file = open('test.json', 'w+b')
		self.exporter = JsonItemExporter(self.file)
		self.exporter.start_exporting()

	def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):

		try:
			index = self.start_urls.index( item['surl'] )
			groupId = index / self.cols
			r = index % self.cols
			if r == 0:
				item['main'] = 0
			elif r == 1:
				item['main'] = 1
			elif r == 2:
				item['main'] = 2
			item['gid'] = groupId
		except:
			index = -1

		self.exporter.export_item(item)
		return item		


class ExcelPipeline(object):

	def __init__(self):
		pass

	def open_spider(self, spider):
		file_name = spider.export_file_name if spider.export_file_name else spider.name + datetime.now().strftime('%Y%m%d_%H-%M-%S')
		self.excel = ExportExcelEveryItem( file_name )

	def process_item(self, item, spider):
		# listitem = self.get_listform_item( item )
		# self.excel.add_item( listitem )
		self.excel.add_item( item )
		return item

	def close_spider(self, spider):
		self.excel.export()

	def get_listform_item(self, item):
		rto = []

		if item:
			rto = [
				item.get('itemId', ''),
				item.get('name', ''),
				item.get('brand', ''),
				item.get('category', ''),
				item.get('url', ''),
				item.get('price', ''),
				item.get('comment', ''),
			]
			if item.get('source') == 'tmall':
				rto.append( item.get('tm_moonSellCount', ''))

			# Information about other SKU
			# if 'relateSKU' in item:
			# 	for sku in item['relateSKU'].keys():
			# 		price = item['relateSKU'][sku].get('price', 0)
			# 		promotionList = item['relateSKU'][sku].get('promotionList', None)
			# 		if type(promotionList) == list and len(promotionList) > 0:
			# 			min_price = sys.maxint
			# 			for i in range( len(promotionList) ):
			# 				if promotionList[i].get('price') and float(promotionList[i].get('price')) < min_price:
			# 					min_price = float(promotionList[i].get('price'))
			# 			price = min_price
			# 		rto.append( sku + '￥' + str(price) )

			for i in item.get('attr'):
				rto.append( i + ':' + item['attr'][i] )

		return rto
				