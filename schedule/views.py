# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

from TestTimer import TestTimer


def schedule_index(request):

	return HttpResponse('schedule_index')


def run(request):
	t = TestTimer(h, sleep=3)
	t.run()
	return HttpResponse('finish')


def h():
	t = TestTimer()
	t.stop()
	print "hahaha"