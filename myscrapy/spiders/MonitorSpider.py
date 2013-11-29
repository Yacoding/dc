# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from myscrapy.items import ProductItem

from urllib import unquote

import re
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')


class MonitorSpider(BaseSpider):

	name = "monitorspider"
	allowed_domains = [ "tmall.com", "taobao.com",
						"jd.com", "3.cn",
						"feifei.com" ]

	start_urls = [
		# 'http://item.feifei.com/E8902592.html',
		# 'http://item.jd.com/563149.html',
		# 'http://chaoshi.detail.tmall.com/item.htm?spm=0.0.0.0.IgipBr&id=12388052828&cat_id=2'
	]

	cols = 0


	def __init__(self, *args, **kwargs):

		super(MonitorSpider, self).__init__(*args, **kwargs)

		urls_group = kwargs.get('urls_group', [[]])
		self.start_urls = self.init_start_urls( urls_group )
		self.cols = len( urls_group[0] )


	def init_start_urls(self, urls_group):

		rto = []

		for i in urls_group:
			rto += i

		return rto


	def parse(self, response):
		""" Main parse function
		"""
		url = response.url

		if url.find( 'tmall.com' ) > -1:
			return self.parseTmall( response )
		elif url.find( 'jd.com' ) > -1:
			return self.parseJd( response )
		elif url.find( 'feifei.com' ) > -1:
			return self.parseFeifei( response )
		else:
			return


	######
	#
	# Tmall parser
	#		

	def parseTmall(self, response):
		""" Tmall parser
		"""
		sel = Selector(response)
		item = ProductItem()  

		item['surl']	= response.url
		item['source']  = 'tmall'       
		item['name']    = self.get_product_name( sel )        

		try:
			# 获取TShop字符串，并对TShop字符串进行JSON标准化处理
			TShop_str = sel.re('TShop\.Setup\(((.|\n)+?)\);')[0]
			# 移除注释，目前只有天猫超市有注释，以逗号开头
			regex = re.compile(',\s*\/\/[^\n]*')
			TShop_str = re.sub(regex, ',', TShop_str)
			TShop = eval( TShop_str, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))() )      
		except SyntaxError:
			return  

		item['itemId']  = TShop.get('itemDO').get('itemId', '')
		item['url']     = 'http://detail.tmall.com/item.htm?id=' + item['itemId']

		initApi_url = TShop.get('initApi')

		yield Request(  initApi_url, 
		                headers={'Referer': 'http://www.google.com.hk/'}, 
		                meta={'item': item}, 
		                callback=self.parse_initapi )


	def parse_initapi(self, response):
		""" 处理initApi的链接
		"""
		item = response.meta['item']
		try:
		    initObj = eval( response.body.strip().decode('gbk'), type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))() )
		    priceInfo = initObj.get('defaultModel').get('itemPriceResultDO').get('priceInfo')
		    item['price'] = self.get_default_price(priceInfo)
		    item['tm_moonSellCount'] = initObj.get('defaultModel').get('sellCountDO').get('sellCount', 0)
		except:
		    print response.body
		finally:
		    yield Request( 'http://dsr.rate.tmall.com/list_dsr_info.htm?itemId=' + item['itemId'],
		                    meta={'item': item},
		                    callback=self.parse_comment )


	def parse_comment(self, response):
		""" 处理获取评论数的链接
		"""
		item = response.meta['item']
		comment = re.findall('rateTotal\":(\d+)', response.body)[0]
		item['comment'] = int(comment) if comment.isdigit() else 0
		yield item


	def get_product_name(self, sel):
		""" 获取商品名
		"""
		name_node = sel.xpath('//div[@id="J_DetailMeta"]//h3')

		if len(name_node.xpath('./a')) > 0:
		    return name_node.xpath('./a/text()').extract()[0]
		elif len(name_node.xpath('./a')) == 0:
		    return name_node.xpath('./text()').extract()[0]
		else:
		    return ''


	def get_default_price(self, priceInfo):
		""" 计算商品的默认价格
		"""
		def_obj = priceInfo.get('def', None)

		if def_obj:
		    # 有Def属性
		    promotionList = def_obj.get('promotionList', None)
		    if type(promotionList) == list and len(promotionList) > 0:
		        # 有促销信息
		        min_price = sys.maxint
		        for i in range( len(promotionList) ):
		            if promotionList[i].get('price') and float(promotionList[i].get('price')) < min_price:
		                min_price = float(promotionList[i].get('price'))
		        return min_price
		    else:
		        # 没促销信息
		        return float(def_obj.get('price'))
		else:
		    # 没有def属性
		    for sku in priceInfo:
		        promotionList = priceInfo[sku].get('promotionList', None)
		        if type(promotionList) == list and len(promotionList) > 0:
		            # 有促销信息
		            min_price = sys.maxint
		            for i in range( len(promotionList) ):
		                if promotionList[i].get('price') and float(promotionList[i].get('price')) < min_price:
		                    min_price = float(promotionList[i].get('price'))
		            return min_price
		        else:
		            # 没促销信息
		            return float(priceInfo[sku].get('price'))


	######
	#
	# Jd parser
	#

	def parseJd(self, response):
		""" Jd parser
		"""
		sel = Selector(response)
		item = ProductItem()

		item['surl']	= response.url
		item['source'] = 'jd'
		item['name'] = sel.xpath("//div[@id='name']//h1/text()").extract()[0] 
		item['url'] = response.url
		item['itemId'] = self.getSku( response.url )

		# return item
		yield Request(  'http://p.3.cn/prices/get?skuid=J_' + item['itemId'],  
		                meta={'item': item}, 
		                callback=self.parsePrice )


	def parsePrice(self, response):	
		item = response.meta['item']
		rto = json.loads( response.body )[0]
		item['price'] = float(rto.get('p', 0))
		yield Request(  'http://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId=' + item['itemId'] + '&callback=getCommentCount',  
		                meta={'item': item}, 
		                callback=self.parseComment )


	def parseComment(self, response):
		item = response.meta['item']
		regex = re.compile('\{.*\}')
		result = regex.search( response.body )
		if result:			
			rto = json.loads( result.group(0) )
			item['comment'] = int(rto.get('CommentCount', 0))
		else:
			item['comment'] = 0
		return item


	def getSku(self, url):
		regex = re.compile( '\/(\d+)\.htm' )
		result = regex.search( url )
		return result.group(1) if result else ''
			

	######
	#
	# Tmall parser
	#	

	def parseFeifei(self, response):
		""" Feifei parser
		"""
		sel = Selector(response)
		item = ProductItem()

		item['surl']	= response.url
		item['source'] 	= 'feifei'
		item['name'] 	= sel.xpath("//h2[@class='np-intro-title']/text()").extract()[0] 
		item['url'] 	= response.url
		item['price'] 	= sel.xpath("//dd[@class='price-m']/text()").extract()[0]

		return item