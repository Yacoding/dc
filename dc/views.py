# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

import datetime
 
def index(request):
	return render_to_response('index.html', context_instance=RequestContext(request)) 

def current_datetime(request):
    current_date = datetime.datetime.now()
    # return render_to_response('current_date.html', {'current_date': current_date})
    # Using locals() All vars are assigned to template
    return render_to_response('radar_index.html', locals())

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)