# -*- coding: utf-8 -*-

import os
import sys
import pymongo
from datetime import datetime
from myscrapy.export import ExportExcelEveryItem



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
				