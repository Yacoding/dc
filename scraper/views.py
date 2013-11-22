# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

import json
import pymongo
from utils.helper import *
import re

from scraper.ScrapyStarter import ScrapyStarter


def scraper_index(request):
	META_TITLE = "Scraper Module"
	return render_to_response('scraper_index.html', locals())


def crawl(request):
	""" receive JSON data only
	"""
	params = get_JSON_request_params(request)

	source = params.get('source')
	tasks = params.get('tasks')
	
	BASE_TM_LIST_URL = "http://list.tmall.com/search_product.htm?cat="

	# check source
	if not source:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'without source' }) )
	elif source.upper() not in ['TM', 'JD']:
		return HttpResponse( to_json({ 'status': 'fail', 'err': 'unknow source' }) )
	
	# deal with start_urls
	start_urls = []
	if source.upper() == 'TM':
		regex = re.compile('cat=(\d+)')		
		for t in tasks:
			result = regex.search( t['start_url'] )
			if result: 
				t['start_url'] = BASE_TM_LIST_URL + result.group(1)
				start_urls.append( (t['category'], t['start_url']) )
	elif source.upper() == 'JD':
		pass

	scrapy = ScrapyStarter()
	scrapy.create( source.upper(), start_urls )
	# scrapy.run()

	return HttpResponse('finish')


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


