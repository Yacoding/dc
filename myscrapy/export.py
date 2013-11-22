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
		self.EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'download')


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

			header = self.get_header()
			self.items[key].insert( 0, header )

			# items loop
			for row in range(0, min(limit, len(self.items[key]))):
				# column loop
				for col in range(0, len(self.items[key][row])):
					self.ws[key].write( row, col, self.items[key][row][col] )

		# save file
		path = os.path.join( self.EXCEL_PATH, self.file + '.xls' )
		self.wb.save( path )


	def get_header(self):

		return [u'商品ID', u'商品名', u'品牌', u'目录', u'链接', u'价格', u'评论数', u'月销量']
