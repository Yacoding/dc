# -*- coding: utf8 -*-
from mongoengine import *
from products.main.BaseModel import Products


class Category(Document):

	meta = {
		"collection" : "category"
	}		


class tmall(Document, Products):

	meta = {
		"collection" : "tmall",
	}


class travel_bags(Document, Products):

	meta = {
		"collection" : "travel_bags",
	}


class men_skin_care(Document, Products):

	meta = {
		"collection" : "men_skin_care",
	}


class washing_care(Document, Products):

	meta = {
		"collection" : "washing_care",
	}


class kitchen_appliances(Document, Products):

	meta = {
		"collection" : "kitchen_appliances",
	}


class live_appliances(Document, Products):

	meta = {
		"collection" : "live_appliances",
	}


class personal_care(Document, Products):

	meta = {
		"collection" : "personal_care",
	}


class furniture(Document, Products):

	meta = {
		"collection" : "furniture",
	}


class lighting(Document, Products):

	meta = {
		"collection" : "lighting",
	}


class kitchen_renovation(Document, Products):

	meta = {
		"collection" : "kitchen_renovation",
	}


class hardware_electrician(Document, Products):

	meta = {
		"collection" : "hardware_electrician",
	}	


class textile(Document, Products):

	meta = {
		"collection" : "textile",
	}	


class winter_bedding(Document, Products):

	meta = {
		"collection" : "winter_bedding",
	}		


class cloth_decoration(Document, Products):

	meta = {
		"collection" : "cloth_decoration",
	}	


class home_accessories(Document, Products):

	meta = {
		"collection" : "home_accessories",
	}	


class home_daily(Document, Products):

	meta = {
		"collection" : "home_daily",
	}	 


class kitchen_dining(Document, Products):

	meta = {
		"collection" : "kitchen_dining",
	}	


class planning_supplies(Document, Products):

	meta = {
		"collection" : "planning_supplies",
	}		
		