# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

from products.main.CollectionFactory import CollectionFactory
from products.main.OperationStrategy import OperationContext
from products.models import Category

import json


# def index(request):
# 	return render_to_response('index.html', context_instance=RequestContext(request)) 

def test(request):
	META_TITLE = "测试页面"
	return render_to_response('test.html', locals())


def radar_index(request):
	"""Mian page of product radar"""
	META_TITLE = "商品雷达"
	MODULE = "radar"
	return render_to_response('radar_index.html', locals())


def radar_detail(request):
	"""Detail page of product radar"""
	META_TITLE = "商品雷达 - 商品详情"
	return render_to_response('radar_detail.html', locals())


def get_category(request):
	"""Get Tmall/JD category"""
	params = _get_request_params( request )
	category = Category.objects.limit(1).all_fields().to_json()
	return HttpResponse( _rto_unify( category, True ) )


def select_products(request):
	"""Select products"""
	params = _get_request_params( request )
	params = _business_unify( params )
	## Strategy action, get products
	return OperationContext.strategy(params.get("operation"), params).action()
	

### Helper Methods ###

def _get_request_params(request):
	params = {}
	if request.method == "GET":
		for param in request.GET:
			params[param] = request.GET.get(param)
	else:
		for param in request.POST:
			params[param] = request.POST.get(param)
	## utf8 encode
	params = _params_utf8_encode( params )
	return params


def _params_utf8_encode(params):
	for i in params:
		params[i] = params[i].encode('utf8')
	return params


def _business_unify(params):
	# items
	if params.has_key("items") and params["items"]:
		params["items"] = params["items"].encode().split(",")
	else: params["items"] = []
	# page
	if not params.has_key("page") or not params["page"]:
		params["page"] = 1
	# operation
	if not params.has_key("operation"):
		params["operation"] = "SHOW_PRODUCTS"
	# collection
	if not params.has_key("collection") or not params["collection"]:
		params["collection"] = "default"
	# sort
	params["sort"] = _get_sort_param( params )
	return params


def _get_sort_param(params):
	sort = params.get("sort")
	if params["source"] == "tmall":
		if "价格" == sort: params["sort"] = "-pro_price"
		elif "销量" == sort: params["sort"] = "-pro_moonsellcount"
		else: params["sort"] = "-pro_price"
	elif params["source"] == "jingdong":
		if "评论数" == sort: params["sort"] = "-pro_comment.评论数"
		elif "价格" == sort: params["sort"] = "-pro_price"
		else: params["sort"] = "-pro_price"
	return params["sort"] 


def _rto_unify(json_obj, first=False):
	unicode_JSON = json.loads( json_obj )
	if first:
		unicode_JSON = unicode_JSON[0]
	unicode_JSON = _remove_id_attribute( unicode_JSON )
	return json.dumps(unicode_JSON, ensure_ascii=False)


def _remove_id_attribute(json_obj):
	if isinstance( json_obj, list ):
		[ _remove_id_attribute(item) for item in json_obj ]
	else:
		if json_obj["_id"]:
			del( json_obj["_id"] )
	return json_obj