# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

import os
import json
import pymongo
from utils.helper import *
import re

from scraper.ScrapyStarter import ScrapyStarter


def scraper_index(request):
	META_TITLE = "网页爬虫"
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

		# regex = re.compile('cat=(\d+)')		
		# for t in tasks:
		# 	result = regex.search( t['start_url'] )
		# 	# has cat attribute
		# 	if result: 
		# 		t['start_url'] = BASE_TM_LIST_URL + 'cat=' + result.group(1)
		# 		start_urls.append( (t['category'], t['start_url']) )
		# 	# without cat attribute
		# 	else:
		# 		regexQ = re.compile('\?q=([^&]+)')
		# 		resultQ = regexQ.search( t['start_url'] )
		# 		if resultQ:
		# 			t['start_url'] = BASE_TM_LIST_URL + 'q=' + resultQ.group(1)
		# 			start_urls.append( ('', t['start_url']) )
	elif source.upper() == 'JD':
		pass

	scrapy = ScrapyStarter()
	scrapy.create( source.upper(), action_type=action_type, start_urls=start_urls )
	scrapy.run()

	if action_type.upper() == 'DEF_CALL':
		return HttpResponse('finish')
	elif action_type.upper() == 'BUSINESS_CALL':
		export_file_name = scrapy.get_export_file_name()
		# export_file_name, export_file_content = scrapy.get_file_name_and_content()
		# if export_file_name:
		# 	response = HttpResponse( export_file_content, "application/vnd.ms-excel" )
		# 	response['Content-Disposition'] = 'attachment; filename=%s' % 'products.xls'
		# 	return response
		# else:
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
	print file_name
	print os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download')
	file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'download', file_name )

	excel_file = open(file_path, "rb")
	file_content = excel_file.read()
	excel_file.close()

	response = HttpResponse( file_content, "application/vnd.ms-excel" )
	response['Content-Disposition'] = 'attachment; filename=%s' % file_name
	return response