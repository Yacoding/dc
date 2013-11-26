# -*- coding: utf8 -*-
import xlwt
import sys
from datetime import datetime
import os


class ExportExcelEveryItem( object ):

	def __init__(self, file_name=datetime.now().strftime('%Y%m%d_%H-%M-%S')):
		self.file = file_name
		self.items = { 'def': [] }
		# workbook instance
		self.wb = xlwt.Workbook()
		self.ws = {}
		self.EXCEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download')


	def add_item(self, item, item_collection='def'):

		if not self.is_items_collection_exist( item_collection ):
			self.create_item_collection( item_collection )
			
		self.items[item_collection].append( item )


	def is_items_collection_exist(self, collection):

		return True if collection in self.items else False


	def create_item_collection(self, collection):

		self.items[collection] = []


	def export(self, limit=sys.maxint):

		# items collection loop
		for key in self.items.keys():

			self.ws[key] = self.wb.add_sheet( key )

			queue = self.walk_products( self.items[key] )

			for row in range(0, min(limit, len(queue))):
				# column loop
				for col in range(0, len(queue[row])):
					self.ws[key].write( row, col, queue[row][col] )

			# header = self.get_header()
			# self.items[key].insert( 0, header )

			# items loop
			# for row in range(0, min(limit, len(self.items[key]))):
			# 	# column loop
			# 	for col in range(0, len(self.items[key][row])):
			# 		self.ws[key].write( row, col, self.items[key][row][col] )

		# save file
		path = os.path.join( self.EXCEL_PATH, self.file + '.xls' )
		self.wb.save( path )


	def walk_products(self, products):
		"""Trival products"""
		header_map = self.get_header_map()
		header = header_map.values()
		package = []
		for product in products:
			tmp = {}
			# Get fixed items
			for item in header_map:
				tmp[ header_map[item] ] = product[item]
			# Get unfixed items
			for it in product["attr"]:
				if it not in header:
					header.append( it )
				tmp[it] = product["attr"][it]
			# Add to package
			package.append( tmp )
		return self._merge_products( header, package )


	def _merge_products(self, header, package):
		"""Merge header and products into array"""
		content = []
		content.append( header )
		for product in package:
			tmp = []
			for i in header:
				if i in product:
					tmp.append( product[i] )
				else: tmp.append( '' )
			content.append( tmp )
		return content	


	def get_header_map(self):

		return {
			u'itemId' : u'商品ID',
			u'name' : u'商品名',
			u'brand' : u'品牌',
			u'category' : u'目录',
			u'url' : u'链接',
			u'price' : u'价格',
			u'comment' : u'评论数',
			u'tm_moonSellCount' : u'月销量'
		}


	def get_header_for_key(self):

		return [u'itemId', u'name', u'brand', u'category', u'url', u'price', u'comment', u'tm_moonSellCount']