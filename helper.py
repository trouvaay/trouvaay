#!/usr/bin/python
import requests
from django.db import models
from django.conf import settings
import cloudinary
cloudinary.config(
  cloud_name = 'trouvaay',  
  api_key = '239337878822387',  
  api_secret = 'sYSwTRGE6LwUnEkb6MgHIlo-tAU'  
)
from cloudinary.models import CloudinaryField

class AbstractImageModel(models.Model):
	is_main = models.BooleanField(default=False)
	image = CloudinaryField('image')
	# size_type = models.Charfield()  need to add choices for thumb, tile, and large
	
	class Meta:
		abstract = True
		app_label = 'goods'

def MakeSlug(string,spaceChar='+',Maxlen=None):
            stringlst = string.split(" ")
            newStr =""
            for word in stringlst:
                newStr+=(word+spaceChar)        
            return newStr[:-1][:Maxlen]

def GeoCode(street, city, state, zipcd, street2=None):
	base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
	zipcd = str(zipcd)
	if street2:
		address = (street+street2+city+state+zipcd)
	else:
		address = (street+city+state+zipcd)
    
	geo_str = MakeSlug(address)    
	key = settings.GOOG_MAP_KEY
	final_url = base_url+"sensor=false"+"&address="+address+"&key="+key    
	
	try:
		r = requests.get(final_url) 
		myobject =  r.json()
		numResults = len(myobject["results"])        
		if myobject['status'] == "OK" and numResults <= 4:
#   	    print 'pulled succesfully from goog with {} elements - thx Serg!'.format(numResults)
			lat = myobject["results"][0]["geometry"]["location"]["lat"]
			lng = myobject["results"][0]["geometry"]["location"]["lng"]
			return(lat,lng)
		else:
			return(None,None)
	except:
		return(None,None)
	

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

Attributes = {
	'segment': [
		('new','new'),
		('vintage','vintage')
	],
	'style': [
		('modern','modern'),
		('traditional', 'traditional'),
		('contemporary', 'contemporary'),
		('rustic', 'rustic'),
		('industrial', 'industrial'),
		('beach', 'beach'),
		],
	'category': [
		('living', 'living'),
		('dining', 'dining'),
		('bedroom', 'bedroom'),
		('office', 'office'),
		('lightning','lightning'),
		('decor','decor'),
        ('other', 'other'),
	],
	'subcategory': [
		('bar', 'bar'),
		('bar_stool','bar_stool'),
		('bed','bed'),
		('bedding','bedding'),
		('bench','bench'),
		('chair','chair'),
		('chaise','chaise'),
		('desk','desk'),
		('desk_light','desk_light'),
		('dining_table','dining_table'),
		('floor_lamp','floor_lamp'),
		('kitchen_serving','kitchen_serving'),
		('loveseat','loveseat'),
		('media','media'),
		('mirror','mirror'),
		('nightstand','nightstand'),
		('ottoman','ottoman'),
		('other_lighting','other_lighting'),
		('pillow','pillow'),
		('rug_throw','rug_throw'),
		('small_table','small_table'),
		('sofa','sofa'),
		('storage','storage'),
		('wall_decor','wall_decor'),
	],
	'material': [
		('acrylic','acrylic'),
		('cotton','cotton'),
		('engineered_wood','engineered_wood'),
		('leather','leather'),
		('linen','linen'),
		('other_fabric','other_fabric'),
		('polyester','polyester'),
		('wood_veneer','wood_veneer'),
	]
}
