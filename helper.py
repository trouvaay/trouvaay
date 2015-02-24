#!/usr/bin/python
import requests
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.conf import settings
from django.contrib.sites.models import RequestSite, Site
from django.template.loader import render_to_string
import cloudinary
from cloudinary.models import CloudinaryField
from math import acos, cos, radians, sin
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
import time


# TODO: convert to environ var
cloudinary.config(
    cloud_name='trouvaay',
    api_key='239337878822387',
    api_secret='sYSwTRGE6LwUnEkb6MgHIlo-tAU'
)


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


def is_time_to_show_modal(request, key):
    """Checks whether it's time to show modal screen"""
    right_now = int(time.mktime(time.localtime()))  # current time time in seconds since epoch
    expiration = int(request.session.get(key, 0))  # exporation time in seconds since epoch
    return expiration < right_now


def hide_modal(request, key, expiration_in_seconds):
    """Sets new value for the cookie key as the expiration time"""
    right_now = int(time.mktime(time.localtime()))
    new_expiration = right_now + expiration_in_seconds
    request.session[key] = str(new_expiration)


def send_email_from_template(to_email, context, subject_template, plain_text_body_template, html_body_template=None):
    """Creates email from subject and body templates and sends message to the user
    
    to_email - recipient email 
    context - dictionary passed to all the templates
    subject_template - template that will be used to generate message subject
    plain_text_body_template - template that will be used to generate plain text message body
    html_body_template - template that will be used to generate html message body
    """
    
    subject = render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines()) # remove new lines from subject
    
    message_txt = render_to_string(plain_text_body_template, context)
    email_message = EmailMultiAlternatives(subject=subject, 
                                           body=message_txt, 
                                           from_email=settings.DEFAULT_FROM_EMAIL, 
                                           to=[to_email], 
                                           bcc=[settings.DEFAULT_FROM_EMAIL])

    if(html_body_template):
        message_html = render_to_string(html_body_template, context)
        email_message.attach_alternative(message_html, 'text/html')
    email_message.send()


def send_user_password_change_email(request, user):
    email_context = {
                     'site': get_site(request),
                     'token': default_token_generator.make_token(user),
                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                     'domain':get_current_site(request).domain,
                     'protocol': 'https' if request.is_secure() else 'http'
                     }

    send_email_from_template(to_email=user.email, context=email_context,
        subject_template='members/implicit_user_creation/email_subject.txt',
        plain_text_body_template='members/implicit_user_creation/email_body.txt',
        html_body_template='members/implicit_user_creation/email_body.html')

def send_order_email(request, order_item, show_password_reset_link, is_buy):
    capture_date = None
    if(order_item.capture_time and not not order_item.captured):
        capture_date = order_item.capture_time.date()

    email_context = {
                     'is_buy': is_buy,
                     'product': order_item.product,
                     'site': get_site(request),
                     'capture_date': capture_date
                     }

    if(show_password_reset_link):
        # This is a newly created user without password. We will send this
        # user a password reset link along with the order
        # add extra context parameters needed for password reset link
        email_context['token'] = default_token_generator.make_token(order_item.order.authuser)
        email_context['uid'] = urlsafe_base64_encode(force_bytes(order_item.order.authuser.pk))
        email_context['domain'] = get_current_site(request).domain
        email_context['protocol'] = 'https' if request.is_secure() else 'http'


    send_email_from_template(to_email=order_item.order.authuser.email, context=email_context,
        subject_template='members/purchase/reserve_confirmation_email_subject.txt',
        plain_text_body_template='members/purchase/reserve_confirmation_email_body.txt',
        html_body_template='members/purchase/reserve_confirmation_email_body.html')

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip

def get_client_id(request):
    client_id = request.session.get('cid', None)
    if(not client_id):
        client_id = get_ip(request)
    return client_id

def get_site(request):
    if Site._meta.installed:
        site = Site.objects.get_current()
    else:
        site = RequestSite(request)    
    return site

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

def getdist(self, ThereLat, ThereLng, HereLat, HereLng):
    """ Calculates distance between two points
    """
    dist = 3959 * acos(cos(radians(HereLat)) * cos(radians(There.lat))
        * cos(radians(There.lng) - radians(HereLng)) + sin(radians(HereLat))*
        sin(radians(There.lat)))      
    return round(dist,2)
# used to determine if AuthUser 'in_coverage_area' field should be set to True
coverage_area = [94040]

# Neigborhoods by google's locality address component
Neighborhoods = {'SF': [
    ('Alameda', 'Alameda'),
    ('Alamo Square', 'Alamo Square'),
    ('Anza Vista', 'Anza Vista'),
    ('Ashbury Heights', 'Ashbury Heights'),
    ('Balboa Terrace', 'Balboa Terrace'),
    ('Bayview - Hunters Point', 'Bayview - Hunters Point'),
    ('Berkeley', 'Berkeley'),
    ('Bernal Heights', 'Bernal Heights'),
    ('Buena Vista', 'Buena Vista'),
    ('Castro', 'Castro'),
    ('Chinatown', 'Chinatown'),
    ('Civic Center', 'Civic Center'),
    ('Cole Valley', 'Cole Valley'),
    ('Corona Heights', 'Corona Heights'),
    ('Cow Hollow', 'Cow Hollow'),
    ('Crocker-Amazon', 'Crocker-Amazon'),
    ('Diamond Heights', 'Diamond Heights'),
    ('Dogpatch', 'Dogpatch'),
    ('Duboce Triangle', 'Duboce Triangle'),
    ('Embarcadero', 'Embarcadero'),
    ('Emeryville', 'Emeryville'),
    ('Excelsior', 'Excelsior'),
    ('Fillmore', 'Fillmore'),
    ('Financial District', 'Financial District'),
    ("Fisherman's Wharf", "Fisherman's Wharf"),
    ('Forest Hill', 'Forest Hill'),
    ('Glen Park', 'Glen Park'),
    ('Haight-Ashbury', 'Haight-Ashbury'),
    ('Hayes Valley', 'Hayes Valley'),
    ('Ingleside', 'Ingleside'),
    ('Ingleside Terraces', 'Ingleside Terraces'),
    ('Inner Sunset', 'Inner Sunset'),
    ('Jackson Square', 'Jackson Square'),
    ('Japantown', 'Japantown'),
    ('Lakeside', 'Lakeside'),
    ('Lakeshore', 'Lakeshore'),
    ('Laurel Heights', 'Laurel Heights'),
    ('Lower Haight', 'Lower Haight'),
    ('Lower Pacific Heights', 'Lower Pacific Heights'),
    ('Lower Nob Hill', 'Lower Nob Hill'),
    ('Marina', 'Marina'),
    ('Merced Heights', 'Merced Heights'),
    ('Merced Manor', 'Merced Manor'),
    ('Miraloma Park', 'Miraloma Park'),
    ('Mission Bay', 'Mission Bay'),
    ('The Mission', 'The Mission'),
    ('Mission Terrace', 'Mission Terrace'),
    ('Monterey Heights', 'Monterey Heights'),
    ('Mount Davidson', 'Mount Davidson'),
    ('Mountain View', 'Mountain View'),
    ('Nob Hill', 'Nob Hill'),
    ('Noe Valley', 'Noe Valley'),
    ('North Beach', 'North Beach'),
    ('NoPa', 'NoPa'), 
    ('Oakland', 'Oakland'),
    ('Oceanview', 'Oceanview'),
    ('Outer Mission', 'Outer Mission'),
    ('Outer Sunset', 'Outer Sunset'),
    ('Outer Richmond', 'Outer Richmond'),
    ('Pacific Heights', 'Pacific Heights'),
    ('Parkmerced', 'Parkmerced'),
    ('Parkside', 'Parkside'),
    ('Portola', 'Portola'),
    ('Potrero Hill', 'Potrero Hill'),
    ('Presidio', 'Presidio'),
    ('Presidio Heights', 'Presidio Heights'),
    ('Rincon Hill', 'Rincon Hill'),
    ('Russian Hill', 'Russian Hill'),
    ('Saint Francis Wood', 'Saint Francis Wood'),
    ('San Jose', 'San Jose'),
    ('San Mateo', 'San Mateo'),
    ('Sea Cliff', 'Sea Cliff'),
    ('Sherwood Forest', 'Sherwood Forest'),
    ('South Beach', 'South Beach'),
    ('South SF', 'South SF'),
    ('SoMa', 'SoMa'),
    ('Sunnyside', 'Sunnyside'),
    ('Sunset District', 'Sunset District'),
    ('Telegraph Hill', 'Telegraph Hill'),
    ('Tenderloin', 'Tenderloin'),
    ('Twin Peaks', 'Twin Peaks'),
    ('Union Square', 'Union Square'),
    ('Visitacion Valley', 'Visitacion Valley'),
    ('West Portal', 'West Portal'),
    ('Western Addition', 'Western Addition'),
    ('Westwood Highlands', 'Westwood Highlands'),
    ('Westwood Park', 'Westwood Park'),
    ('Yerba Buena', 'Yerba Buena')
]}

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
#     'segment': [
#         ('new','new'),
#         ('vintage','vintage')
#     ],
#     'style': [
#         ('modern','modern'),
#         ('traditional', 'traditional'),
#         ('contemporary', 'contemporary'),
#         ('rustic', 'rustic'),
#         ('industrial', 'industrial'),
#         ('beach', 'beach'),
#         ],
#     'category': [
#         ('living', 'living'),
#         ('dining', 'dining'),
#         ('bedroom', 'bedroom'),
#         ('office', 'office'),
#         ('lightning','lightning'),
#         ('decor','decor'),
#         ('other', 'other'),
#     ],
#     'subcategory': [
#         ('bar', 'bar'),
#         ('bar_stool','bar_stool'),
#         ('bed','bed'),
#         ('bedding','bedding'),
#         ('bench','bench'),
#         ('chair','chair'),
#         ('chaise','chaise'),
#         ('desk','desk'),
#         ('desk_light','desk_light'),
#         ('dining_table','dining_table'),
#         ('floor_lamp','floor_lamp'),
#         ('kitchen_serving','kitchen_serving'),
#         ('loveseat','loveseat'),
#         ('media','media'),
#         ('mirror','mirror'),
#         ('nightstand','nightstand'),
#         ('ottoman','ottoman'),
#         ('other_lighting','other_lighting'),
#         ('pillow','pillow'),
#         ('rug_throw','rug_throw'),
#         ('small_table','small_table'),
#         ('sofa','sofa'),
#         ('storage','storage'),
#         ('wall_decor','wall_decor'),
#     ],
#     'material': [
#         ('acrylic','acrylic'),
#         ('cotton','cotton'),
#         ('engineered_wood','engineered_wood'),
#         ('leather','leather'),
#         ('linen','linen'),
#         ('other_fabric','other_fabric'),
#         ('polyester','polyester'),
#         ('wood_veneer','wood_veneer'),
#     ]
# }


