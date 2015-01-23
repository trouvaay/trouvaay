#!/usr/bin/python
import requests
from django.db import models
from django.conf import settings
import cloudinary

#TODO: convert to environ var
cloudinary.config(
  cloud_name = 'trouvaay',  
  api_key = '239337878822387',  
  api_secret = 'sYSwTRGE6LwUnEkb6MgHIlo-tAU'  
)

from cloudinary.models import CloudinaryField

class AbstractImageModel(models.Model):
	"""Abstract image model for ProductIMage and RetailerIMage models.
	Uses Cloudinary for image rendering
	"""
	#main image will be primary/1st displayed to user
	is_main = models.BooleanField(default=False)
	image = CloudinaryField('image')
	
	class Meta:
		abstract = True
		#primarily used in ProductImage model in goods app
		app_label = 'goods'

def MakeSlug(string,spaceChar='+',Maxlen=None):
	"""for use in GeoCode fct below"""
	stringlst = string.split(" ")
	newStr =""
	for word in stringlst:
		newStr+=(word+spaceChar)		
	return newStr[:-1][:Maxlen]

def GeoCode(street, city, state, zipcd, street2=None):
	"""Used to fetch lat/lng coords from google api

	"""
	
	base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
	zipcd = str(zipcd)
	
	if street2:
		address = (street+street2+city+state+zipcd)
	else:
		address = (street+city+state+zipcd)
	
	# address slug
	geo_str = MakeSlug(address)
	#TODO: convert to google API key to evrion var 
	key = settings.GOOG_MAP_KEY
	final_url = base_url+"sensor=false"+"&address="+address+"&key="+key	
	try:
		r = requests.get(final_url) 
		location_object =  r.json()
		num_results = len(location_object["results"])
		# if response is 200 status and they arent too many results	   
		if location_object['status'] == "OK" and num_results <= 4:
			lat = location_object["results"][0]["geometry"]["location"]["lat"]
			lng = location_object["results"][0]["geometry"]["location"]["lng"]
			return(lat,lng)
		else:
			return(None,None)
	except:
		return(None,None)

# used to determine if AuthUser 'in_coverage_area' field should be set to True
coverage_area = [94040]

States = [
		('AK', 'Alaska'),
		('AL', 'Alabama'),
		('AR', 'Arkansas'),
		('AS', 'American Samoa'),
		('AZ', 'Arizona'),
		('CA', 'California'),
		('CO', 'Colorado'),
		('CT', 'Connecticut'),
		('DC', 'District of Columbia'),
		('DE', 'Delaware'),
		('FL', 'Florida'),
		('GA', 'Georgia'),
		('GU', 'Guam'),
		('HI', 'Hawaii'),
		('IA', 'Iowa'),
		('ID', 'Idaho'),
		('IL', 'Illinois'),
		('IN', 'Indiana'),
		('KS', 'Kansas'),
		('KY', 'Kentucky'),
		('LA', 'Louisiana'),
		('MA', 'Massachusetts'),
		('MD', 'Maryland'),
		('ME', 'Maine'),
		('MI', 'Michigan'),
		('MN', 'Minnesota'),
		('MO', 'Missouri'),
		('MP', 'Northern Mariana Islands'),
		('MS', 'Mississippi'),
		('MT', 'Montana'),
		('NA', 'National'),
		('NC', 'North Carolina'),
		('ND', 'North Dakota'),
		('NE', 'Nebraska'),
		('NH', 'New Hampshire'),
		('NJ', 'New Jersey'),
		('NM', 'New Mexico'),
		('NV', 'Nevada'),
		('NY', 'New York'),
		('OH', 'Ohio'),
		('OK', 'Oklahoma'),
		('OR', 'Oregon'),
		('PA', 'Pennsylvania'),
		('PR', 'Puerto Rico'),
		('RI', 'Rhode Island'),
		('SC', 'South Carolina'),
		('SD', 'South Dakota'),
		('TN', 'Tennessee'),
		('TX', 'Texas'),
		('UT', 'Utah'),
		('VA', 'Virginia'),
		('VI', 'Virgin Islands'),
		('VT', 'Vermont'),
		('WA', 'Washington'),
		('WI', 'Wisconsin'),
		('WV', 'West Virginia'),
		('WY', 'Wyoming'),
]


##########################################
# May want to implement Product characterisitcs as choices instead of
# individual models

# Attributes = {
# 	'segment': [
# 		('new','new'),
# 		('vintage','vintage')
# 	],
# 	'style': [
# 		('modern','modern'),
# 		('traditional', 'traditional'),
# 		('contemporary', 'contemporary'),
# 		('rustic', 'rustic'),
# 		('industrial', 'industrial'),
# 		('beach', 'beach'),
# 		],
# 	'category': [
# 		('living', 'living'),
# 		('dining', 'dining'),
# 		('bedroom', 'bedroom'),
# 		('office', 'office'),
# 		('lightning','lightning'),
# 		('decor','decor'),
#		 ('other', 'other'),
# 	],
# 	'subcategory': [
# 		('bar', 'bar'),
# 		('bar_stool','bar_stool'),
# 		('bed','bed'),
# 		('bedding','bedding'),
# 		('bench','bench'),
# 		('chair','chair'),
# 		('chaise','chaise'),
# 		('desk','desk'),
# 		('desk_light','desk_light'),
# 		('dining_table','dining_table'),
# 		('floor_lamp','floor_lamp'),
# 		('kitchen_serving','kitchen_serving'),
# 		('loveseat','loveseat'),
# 		('media','media'),
# 		('mirror','mirror'),
# 		('nightstand','nightstand'),
# 		('ottoman','ottoman'),
# 		('other_lighting','other_lighting'),
# 		('pillow','pillow'),
# 		('rug_throw','rug_throw'),
# 		('small_table','small_table'),
# 		('sofa','sofa'),
# 		('storage','storage'),
# 		('wall_decor','wall_decor'),
# 	],
# 	'material': [
# 		('acrylic','acrylic'),
# 		('cotton','cotton'),
# 		('engineered_wood','engineered_wood'),
# 		('leather','leather'),
# 		('linen','linen'),
# 		('other_fabric','other_fabric'),
# 		('polyester','polyester'),
# 		('wood_veneer','wood_veneer'),
# 	]
# }
