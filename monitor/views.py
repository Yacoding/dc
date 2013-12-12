# -*- coding: utf-8 -*-
import os
import pymongo

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

from monitor import MonitorTemplateHandler, save_tasks_to_mongo
from utils.helper import *


conn = pymongo.Connection('127.0.0.1', 27017)


def monitor(request):
	""" Monitor module's index action
	"""
	META_TITLE = "数据中心 - 价格监控"
	MODULE = "monitor"
	price_list = list( conn['monitor']['result'].find() )
	return render_to_response('monitor_index.html', locals())


def monitor_sku(request, sku):
	""" Monitor information of specific sku

	Parameters
    ----------
    sku : specific sku from url
	"""
	META_TITLE = "数据中心 - 价格监控"
	MODULE = "monitor"
	item = conn['monitor']['result'].find_one({'sku':sku}, {'_id': False})
	extraList = item.get('extraList', {}).values()
	return render_to_response('monitor_item.html', locals())


def monitor_template( request ):
	""" Handle template, require as GET and submit as POST
	"""
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

		t_handler = MonitorTemplateHandler( template )
		tasks = t_handler.explain()		
		save_tasks_to_mongo( conn['monitor']['tasks'], tasks )
		return HttpResponse( to_json({ 'status': 'success' }) )