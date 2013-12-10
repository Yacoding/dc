# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

import os
import json
import pymongo
from utils.helper import *
import re
import xlrd
from datetime import datetime

from scraper.ScrapyStarter import ScrapyStarter


conn = pymongo.Connection('127.0.0.1', 27017)


def scraper_index(request):
	META_TITLE = "数据中心 - 网页爬虫"
	MODULE = "scraper"
	return render_to_response('scraper_index.html', locals())


def scraper_admin(request):
	META_TITLE = "Scraper Module Admin"
	return render_to_response('scraper_admin.html', locals())


def crawl(request):
	""" receive JSON data only
	"""
	params = get_JSON_request_params(request)

	source = params.get('source')
	tasks = params.get('tasks')
	action_type = params.get('type', 'DEF_CALL')
	
	BASE_TM_LIST_URL = "http://list.tmall.com/search_product.htm?"

	# check source
	if not source:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'without source' }) )
	elif source.upper() not in ['TM', 'JD']:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow source' }) )
	elif action_type.upper() not in ['DEF_CALL', 'BUSINESS_CALL']:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow action_type' }) )
	
	# deal with start_urls
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

	scrapy = ScrapyStarter()
	scrapy.create( source.upper(), action_type=action_type, start_urls=start_urls )
	scrapy.run()

	if action_type.upper() == 'DEF_CALL':
		return HttpResponse('finish')
	elif action_type.upper() == 'BUSINESS_CALL':
		export_file_name = scrapy.get_export_file_name()
		return HttpResponse( to_json({ 'status': 'success', 'content': export_file_name }) )


def category(request):

	params = get_request_params(request)

	source = params.get('source')
	action = params.get('action', 'GET')

	if not source:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'without source' }) )
	elif source.upper() not in ['TM', ]:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow source' }) )

	# Update Category Action
	if action.upper() == 'UPDATE':

		if source.upper() == 'TM':
			scrapy = ScrapyStarter()
			scrapy.create( 'tm_cat' )
			scrapy.run()

		elif source.upper() == 'JD':
			pass

		return HttpResponse( to_json({ 'status': 'success' }) )

	# Get Category Action
	elif action.upper() == 'GET':

		if source.upper() == 'TM':
			conn = pymongo.Connection('127.0.0.1', 27017)
			result = conn['test']['cat'].find_one()
			result = remove_id_attribute( result )
			return HttpResponse( to_json({ 'status': 'success', 'content': result }) )

		elif source.upper() == 'JD':
			pass

		return HttpResponse( to_json({ 'status': 'success' }) )

	# Unknow Action
	else:

		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow action' }) )



def get_excel(request):

	params = get_request_params(request)

	file_name = params.get('file_name')
	file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', file_name )

	excel_file = open(file_path, "rb")
	file_content = excel_file.read()
	excel_file.close()

	response = HttpResponse( file_content, "application/vnd.ms-excel" )
	response['Content-Disposition'] = 'attachment; filename=%s' % file_name
	return response


def monitor(request):

	if request.method == "GET":
		META_TITLE = "数据中心 - 价格监控"
		MODULE = "monitor"

		price_list = list( conn['monitor']['result'].find() )

		return render_to_response('monitor_index.html', locals())


def _explainTemplate( xls_name ):

	wb = xlrd.open_workbook( xls_name )
	table = wb.sheet_by_index(0)

	tasks = []
	date = datetime.now().strftime('%Y-%m-%d')

	for i in range(1, table.nrows):

		sku = table.cell(i, 0).value

		if not sku:
			continue

		item = {
			'sku' : sku,
			'date' : date,
			'state' : 1,
			'urls' : [],
			'extras': []
		}

		tm_url = table.cell(i, 1).value
		regex = re.compile('[\?&]id=(\d+)')
		result = regex.search( tm_url )
		if result:
			item['urls'].append( 'http://detail.tmall.com/item.htm?id=%s' % result.group(1) )

		tm_q_url = table.cell(i, 2).value
		if tm_q_url.find('list.tmall.com') > -1:
			regex = re.compile('[\?&]q=([^&]+)')
			result = regex.search( tm_q_url )
			if result:
				item['extras'].append( 'http://list.tmall.com/search_product.htm?q=%s' % result.group(1) )
		elif tm_q_url.find('detail.tmall.com') > -1:
			regex = re.compile('[\?&]id=(\d+)')
			result = regex.search( tm_q_url )
			if result:
				item['extras'].append( 'http://detail.tmall.com/item.htm?id=%s' % result.group(1) )

		for j in range(3, table.ncols):
			if table.cell(i, j).value:
				item['urls'].append( table.cell(i, j).value )

		item['urls'].append( "http://item.feifei.com/%s.html" % sku )

		tasks.append( item )

	os.remove( xls_name )

	return tasks


def _saveToMongo( tasks ):

	coll = conn['monitor']['tasks']

	for task in tasks:

		if coll.find_one( {'sku': task['sku']} ):
			coll.remove( {'sku': task['sku']} )

		coll.insert( task )

	
def monitor_template( request ):

	if request.method == "GET":

		file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', 'monitor_template.xlsx' )

		with open(file_path, "rb") as excel_file:
			file_content = excel_file.read()

		response = HttpResponse( file_content, "application/vnd.ms-excel" )
		response['Content-Disposition'] = 'attachment; filename=monitor_template.xlsx'
		return response

	elif request.method == "POST":
		try:
			template = request.FILES['monitor-template']
		except:
			return HttpResponse( to_json({ 'status': 'fail' }) )
		# save template file
		now = datetime.now().strftime('%Y%m%d_%H-%M-%S')
		UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload')
		xls_name = os.path.join(UPLOAD_PATH, now+template.name)
		with open( xls_name, 'wb+' ) as xls:
			xls.write( template.read() )
		# handle  template file
		tasks = _explainTemplate( xls_name )
		_saveToMongo( tasks )

		return HttpResponse( to_json({ 'status': 'success' }) )


def monitor_sku(request, sku):

	META_TITLE = "数据中心 - 价格监控"
	MODULE = "monitor"

	item = conn['monitor']['result'].find_one({'sku':sku}, {'_id': False})

	extraList = item.get('extraList', {}).values()

	return render_to_response('monitor_item.html', locals())
