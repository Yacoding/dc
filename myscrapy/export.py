# -*- coding: utf8 -*-

class ExportExcel( object ):
	"""docstring for ExportProducts"""
	def __init__(self, products):
		self.products = products

	def action(self):
		# Export products
		content = self._walk_products( self.products )	
		## http response	
		rto = self._export( content )
		# response = HttpResponse( rto, "application/vnd.ms-excel" )
		# response['Content-Disposition'] = 'attachment; filename=%s' % 'products.xls'
		# return response		

	def _init_header(self, source):
		"""Init Excel header for fixed column"""
		if source == "tmall":
			return [u'source', u'name', u'price', u'tm_moonSellCount', u'comment', u'url']
		else:
			return []

	def _walk_products(self, products):
		"""Trival products"""
		headerO = self._init_header( 'tmall' )
		header = self._init_header( 'tmall' )
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
		return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'products.xls')