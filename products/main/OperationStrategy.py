# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod
from products.main.CollectionFactory import CollectionFactory
import json
from math import ceil
import xlwt
import os
from django.http import HttpResponse
from django.shortcuts import render_to_response


class OperationContext:
	@staticmethod
	def strategy(op_code, params):
		if op_code.upper() == "SHOW_PRODUCTS":
			return ShowProducts(params)
		elif op_code.upper() == "DETAIL_PAGE":
			return ProductsDetailPage(params)
		elif op_code.upper() == "PRODUCTS_DETAIL":
			return ShowProductsDetail(params)
		elif op_code.upper() == "EXPORT_PRODUCTS":
			return ExportProducts(params)
		else:
			return OperationStrategy()



class OperationStrategy( object ):
	@abstractmethod
	def action(self):
		pass

	def _rto_unify(self, json_obj, first=False):
		unicode_JSON = json.loads( json_obj )
		if first:
			unicode_JSON = unicode_JSON[0]
		unicode_JSON = self._remove_id_attribute( unicode_JSON )
		return unicode_JSON

	def _remove_id_attribute(self, json_obj):
		if isinstance( json_obj, list ):
			[ self._remove_id_attribute(item) for item in json_obj ]
		else:
			if json_obj["_id"]:
				del( json_obj["_id"] )
		return json_obj



class ShowProducts( OperationStrategy ):
	"""docstring for ShowProducts"""
	PAGE_ITEMS = 50		## Items every page

	def __init__(self, params):
		super(ShowProducts, self).__init__()
		self.params = params

	def action(self):
		rto = { 'products': None, 'page': { 'current': self.params.get("page"), 'total': None } }
		collection = CollectionFactory.factory( self.params.get("collection") )
		## Get page
		rto['page']['total'] = int( ceil( collection.objects.filter(category=self.params.get("category")).count() / self.PAGE_ITEMS ) )
		## Get products
		products_json = collection.objects.filter(category=self.params.get("category")).order_by( self.params.get("sort") ).skip( self.PAGE_ITEMS*(int(self.params.get("page"))-1) ).limit( int(self.PAGE_ITEMS) ).all_fields().to_json()		
		rto['products'] = self._rto_unify( products_json )
		rto = json.dumps(rto, ensure_ascii=False)
		## http response
		return HttpResponse( rto )



class ProductsDetailPage( OperationStrategy ):
	"""Response detail page"""
	def __init__(self, params):
		super(ProductsDetailPage, self).__init__()
		self.params = params

	def action(self):
		self.params["items"] = ",".join( self.params["items"] )
		params = self.params
		return render_to_response('radar_detail.html', locals())
						


class ShowProductsDetail( OperationStrategy ):
	"""docstring for ClassName"""
	def __init__(self, params):
		super(ShowProductsDetail, self).__init__()
		self.params = params

	def action(self):
		collection = CollectionFactory.factory( self.params.get("collection") )
		## Get products
		products_json = collection.objects.filter(sku__in=self.params.get("items")).all_fields().to_json()
		products = self._rto_unify( products_json )
		products = json.dumps(products, ensure_ascii=False)
		## http response
		return HttpResponse( products )
	
		

class ExportProducts( OperationStrategy ):
	"""docstring for ExportProducts"""
	def __init__(self, params):
		super(ExportProducts, self).__init__()
		self.params = params

	def action(self):
		# Get products
		collection = CollectionFactory.factory( self.params.get("collection") )
		if self.params.get("export_all").upper() == "TRUE":
			if self.params.get("category"):
				products = collection.objects.filter(category=self.params.get("category")).order_by( self.params.get("sort") ).limit(6000).all_fields()
			else:
				## http response
				return HttpResponse( "EMPTY CATEGORY" )
		else:
			products = collection.objects.filter(sku__in=self.params.get("items")).all_fields()
		# Export products
		content = self._walk_products( products )	
		## http response	
		rto = self._export( content )
		response = HttpResponse( rto, "application/vnd.ms-excel" )
		response['Content-Disposition'] = 'attachment; filename=%s' % 'products.xls'
		return response		

	def _init_header(self, source):
		"""Init Excel header for fixed column"""
		if source == "tmall":
			return [u'source', u'name', u'category', u'price', u'tm_moonSellCount', u'comment', u'url']
		else:
			return []

	def _walk_products(self, products):
		"""Trival products"""
		headerO = self._init_header( self.params.get("source") )
		header = self._init_header( self.params.get("source") )
		package = []
		for product in products:
			tmp = {}
			# Get fixed items
			for item in headerO:
				tmp[item] = product[item]
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

	def _export(self, content):
		"""Export content array to Excel file"""
		wb = xlwt.Workbook()
		ws = wb.add_sheet('Products Sheet')
		for row in range( 0, len(content) ):
			for col in range( 0, len(content[row]) ):
				ws.write(row, col, content[row][col])
		wb.save( self._excel_path() )
		return self._get_file_content()

	def _get_file_content(self):
		"""Get binary string of excel file"""
		excel_file = open(self._excel_path(), "rb")
		file_content = excel_file.read()
		excel_file.close()
		return file_content

	def _excel_path(self):
		"""Path to excel file"""
		return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download/products.xls')