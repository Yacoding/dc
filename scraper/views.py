# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

import json
from utils.helper import *

from scraper.ScrapyStarter import ScrapyStarter


def scraper_index(request):
	META_TITLE = "Scraper Module"
	return render_to_response('scraper_index.html', locals())


def crawl(request):

	params = get_request_params(request)

	# print dict(params)

	start_url = "http://list.tmall.com/search_product.htm?cat=50916011"

	scrapy = ScrapyStarter()
	# scrapy.create( 'JD', "http://list.jd.com/737-794-798-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-33.html" )
	scrapy.create( 'TM', start_url )
	scrapy.run()

	return HttpResponse('finish')


def update_category(request):

	params = get_request_params(request)

	source = params.get('source')

	if not source:
		return HttpResponse( to_json({ 'status': 'false', 'err': 'without source' }) )
	elif source.upper() not in ['TM', ]:
		return HttpResponse( to_json({ 'status': 'false', 'err': 'unknow source' }) )

	if source.upper() == 'TM':
		scrapy = ScrapyStarter()
		scrapy.create( 'tm_cat' )
		scrapy.run()

	return HttpResponse( to_json({ 'status': 'success' }) )