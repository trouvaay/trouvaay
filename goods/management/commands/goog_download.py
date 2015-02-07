from django.core.management.base import BaseCommand, CommandError
from goods.models import Product, ProductImage, Segment, Subcategory, FurnitureType, Material, add_img_instance
import requests
from pprint import pprint as pp
import gspread
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)

email = 'blakesadams@gmail.com'
password = 'Bloopers1423'


class Command(BaseCommand):
    args = '<goog_file_name spreadsheet_name start_row end_row>'
    help = 'Creats product instances for the given set of rows'

    def handle(self, *args, **options):
        goog_file_name = args[0]
        spreadsheet_name = args[1]
        start_row = int(args[2])
        end_row = int(args[3])

        gc = gspread.login(email, password)
        ss = gc.open(goog_file_name)
        worksheet_list = ss.worksheets()
        worksheet = ss.worksheet(spreadsheet_name)

        headers = [i for i in worksheet.row_values(1)]
        # try:
        for row in range(start_row, end_row+1):
            data = worksheet.row_values(row)
            row_len = len(data)
            print ('data is {} long'.format(len(data)))
            u = Product()

            # Store = data[0]
            u.store_id = int(data[1])
            u.short_name = unicode(data [2]) # for slugify
            u.url = data[3]
            u.is_sold = (True if data[4] == 'True' else False)
            u.original_price = float(data[5])
            u.current_price = float(data[6])
            u.is_custom = (True if data[7] == 'True' else False)
            u.is_floor_model = (True if data[8] == 'True' else False)
            u.description = data[9]
            u.width = (None if data[10] == None else float(data[10]))
            u.depth = (None if data[11] == None else float(data[11]))
            u.height = (None if data[12] == None else float(data[12]))
            u.seat_height = (None if data[13] == None else float(data[13]))
            u.diameter = (None if data[14] == None else float(data[14]))
            u.bed_size = data[15]
            u.weight = (None if data[16] == None else float(data[16]))
            color1 = data[17]
            color2 = data[18]
            u.color_description = data[19]
            u.material_description = data[21]
            u.delivery_weeks = data[25]

            try:
                u.save()
                logger.info('Added {} to database'.format(u))
                u.material.add(Material.objects.get(select=data[20]))
                u.segment.add(Segment.objects.get(select=data[22]))
                u.furnituretype.add(FurnitureType.objects.get(select=data[23]))
                u.subcategory.add(Subcategory.objects.get(select=data[24]))
                main_image_url = data[26]
                try:
                    ProductImage.objects.get(product=u)
                except ProductImage.DoesNotExist:
                    add_img_instance(u.pk, main_image_url, is_main=True)
                
                for i in range(27,30):
                    try:
                        add_img_instance(u.pk, data[i])    
                    except Exception, e:
                        logger.info('No {} Image for {}'.format(headers[i], u))
                        break

            except Exception, e:
                logger.error('Error Saving {} from google into database'.format(u))
                logger.error(str(e))
            

        
        