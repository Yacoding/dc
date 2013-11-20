# -*- coding: utf8 -*-
from products.models import *

class CollectionFactory:

	_collections = {
		'旅行箱包':		travel_bags,
		'男士护肤':     men_skin_care,
		'个人洗护':     washing_care,
		'厨房电器':     kitchen_appliances,
		'生活电器':     live_appliances,
		'个人护理':     personal_care,
		'精品家具':     furniture,
		'灯饰照明':     lighting,
		'厨卫装修':    	kitchen_renovation,
		'五金电工':     hardware_electrician,
		'精品家纺':     textile,
		'冬季床品':     winter_bedding,
		'布艺软饰':     cloth_decoration,    
		'家居饰品':     home_accessories,
		'居家日用':     home_daily,
		'厨房餐饮':     kitchen_dining,
		'计生用品':     planning_supplies,
		'default' : 	tmall,
	}

	@staticmethod
	def factory(collType):
		if CollectionFactory._collections.has_key( collType ):
			return CollectionFactory._collections[collType]
		else:
			return CollectionFactory._collections["default"]
