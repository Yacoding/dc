# -*- coding: utf8 -*-
from mongoengine import *

class Products():
	## fixed fields
	source			= StringField()
	sku				= StringField()
	name 			= StringField()
	category		= ListField()
	attr			= DictField()
	## unfixed fields
	url				= StringField()
	img				= StringField()
	relateSKU		= ListField()
	tm_skuPrice		= DictField()
	tm_postage		= DictField()
	## fields for sort
	comment			= ListField()
	price			= DecimalField()
	date			= DateTimeField()
	tm_moonSellCount= IntField()
	## history
	history			= ListField()

	__class__ = None