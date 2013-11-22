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
		now = datetime.now().strftime('%Y%m%d_%H-%M-%S')
		self.excel = ExportExcelEveryItem( spider.name + now )

	def process_item(self, item, spider):
		listitem = self.get_listform_item( item )
		self.excel.add_item( listitem )
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

			if 'relateSKU' in item:
				for sku in item['relateSKU'].keys():
					price = item['relateSKU'][sku].get('price', 0)
					promotionList = item['relateSKU'][sku].get('promotionList', None)
					if type(promotionList) == list and len(promotionList) > 0:
						min_price = sys.maxint
						for i in range( len(promotionList) ):
							if promotionList[i].get('price') and float(promotionList[i].get('price')) < min_price:
								min_price = float(promotionList[i].get('price'))
						price = min_price
					rto.append( sku + '￥' + str(price) )

			for i in item.get('attr'):
				rto.append( i + ':' + item['attr'][i] )

		# for i in rto:
		# 	if i.__class__ == unicode:
		# 		i = i.encode('utf-8')

		return rto
				