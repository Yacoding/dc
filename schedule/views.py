# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext 

from TestTimer import TestTimer

def h():
	print "hahaha"

t = TestTimer(h, sleep=3)


def schedule_index(request):

	return HttpResponse('schedule_index')


def run(request):
	t.run()
	return HttpResponse('finish')





def stop(request):
	t.stop()
	return HttpResponse('finish')