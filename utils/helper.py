# -*- coding: utf-8 -*-

import json

### Helper Methods ###

def get_JSON_request_params(request):
	
	return json.loads( request.raw_post_data )


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


def remove_id_attribute(json_obj):
	if isinstance( json_obj, list ):
		[ _remove_id_attribute(item) for item in json_obj ]
	else:
		if json_obj["_id"]:
			del( json_obj["_id"] )
	return json_obj