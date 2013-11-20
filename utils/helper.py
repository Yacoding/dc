# -*- coding: utf-8 -*-

import json

### Helper Methods ###

def get_request_params(request):
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


def to_json( obj ):
	return json.dumps( obj, ensure_ascii=False )