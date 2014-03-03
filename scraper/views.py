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

from scraper import ScrapyStarter, get_start_urls


conn = pymongo.Connection('127.0.0.1', 27017)


def scraper_index(request):
	"""Scraper module's index action
	"""
	META_TITLE = "数据中心 - 网页爬虫"
	MODULE = "scraper"
	return render_to_response('scraper_index.html', locals())


def scraper_admin(request):
	"""Scraper module's admin action
	"""
	META_TITLE = "数据中心 - 爬虫后台"
	MODULE = "scraper"
	return render_to_response('scraper_admin.html', locals())


def crawl(request):
	""" receive JSON data only
	"""
	params = get_JSON_request_params(request)
	source = params.get('source')
	tasks = params.get('tasks')
	action_type = params.get('type', 'DEF_CALL')	
	# check source and action
	if not source:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'without source' }) )
	elif source.upper() not in ['TM', 'JD']:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow source' }) )
	elif action_type.upper() not in ['DEF_CALL', 'BUSINESS_CALL']:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow action_type' }) )
	
	start_urls = get_start_urls( source, tasks )
	scrapy = ScrapyStarter()
	scrapy.create( source.upper(), action_type=action_type, start_urls=start_urls )
	scrapy.run()

	if action_type.upper() == 'DEF_CALL':
		return HttpResponse('finish')
	elif action_type.upper() == 'BUSINESS_CALL':
		export_file_name = scrapy.get_export_file_name()
		return HttpResponse( to_json({ 'status': 'success', 'content': export_file_name }) )


def category(request):
	""" Handle category, update as POST and get as GET
	"""
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
	""" Get excel file of scrapy result
	"""
	params = get_request_params(request)
	file_name = params.get('file_name')
	file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', file_name )
	with open(file_path, "rb") as excel_file:
		file_content = excel_file.read()

	response = HttpResponse( file_content, "application/vnd.ms-excel" )
	response['Content-Disposition'] = 'attachment; filename=%s' % file_name
	return response



def monitor(request):

	if request.method == "GET":
		META_TITLE = "商品雷达"
		MODULE = "monitor"
		return render_to_response('monitor_index.html', locals())

	elif request.method == "POST":
		template = request.FILES['monitor-template']
		# save template file
		now = datetime.now().strftime('%Y%m%d_%H-%M-%S')
		UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'upload')
		xls_name = os.path.join(UPLOAD_PATH, now+template.name)
		with open( xls_name, 'wb+' ) as xls:
			xls.write( template.read() )
		# handle  template file
		start_urls = explainTemplate( xls_name )

		crawler = CrawlerStarter( 'MonitorSpider', start_urls=start_urls )
		crawler.start()

		with open('test.json', 'rb') as f:
			rto = f.read()

		return HttpResponse( to_json({ 'status': 'success', 'content': json.loads(rto) }) )

		# return HttpResponse( to_json({ 'status': 'success', 'content': 'sth' }) )


def explainTemplate( xls_name ):
	wb = xlrd.open_workbook( xls_name )
	table = wb.sheet_by_index(0)
	data = []
	for i in range(table.nrows):
		data.append( table.row_values(i) )
	os.remove( xls_name )
	return data


# def explainTemplate( xls_name ):
# 	wb = xlrd.open_workbook( xls_name )
# 	table = wb.sheet_by_index(0)
# 	data = []
# 	for i in range(table.nrows):
# 		data.append( table.row_values(i) )
# 	os.remove( xls_name )
# 	return data
