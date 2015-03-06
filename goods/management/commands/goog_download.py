from django.core.management.base import BaseCommand, CommandError
from goods.models import Product, ProductImage, Segment, Subcategory, FurnitureType, Material, add_img_instance
import requests
from pprint import pprint as pp
import gspread
import logging
from django.db import IntegrityError
from django.conf import settings

logger = logging.getLogger(__name__)

email = settings.GMAIL_EMAIL
password = settings.GMAIL_PASSWORD

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
            
            # try:
            data = worksheet.row_values(row)
            
            # if data[0] == 'TRUE':
            logger.info('uploading {}'.format(data[3]))
            u = Product()

            # Store = data[0]
            u.store_id = int(data[2])
            u.short_name = unicode(data[3]) # for slugify
            u.url = data[4]
            u.is_sold = (True if data[5] == 'True' else False)
            u.original_price = float(data[6])
            u.current_price = float(data[7])
            u.is_custom = (True if data[8] == 'True' else False)
            u.is_floor_model = (True if data[9] == 'True' else False)
            u.description = data[10]
            u.width = (None if data[11] == None else float(data[11]))
            u.depth = (None if data[12] == None else float(data[12]))
            u.height = (None if data[13] == None else float(data[13]))
            u.seat_height = (None if data[14] == None else float(data[14]))
            u.diameter = (None if data[15] == None else float(data[15]))
            u.bed_size = data[16]
            u.weight = (None if data[17] == None else float(data[17]))
            color1 = data[18]
            color2 = data[19]
            u.color_description = data[20]
            u.material_description = data[22]
            u.delivery_weeks = data[26]
            u.is_published = True
            u.save()
            
            if data[21]: u.material.add(Material.objects.get(select=data[21]))
            u.segment.add(Segment.objects.get(select=data[23]))
            u.furnituretype.add(FurnitureType.objects.get(select=data[24]))
            u.subcategory.add(Subcategory.objects.get(select=data[25]))
            main_image_url = data[27]
            
            try:
                ProductImage.objects.get(product=u)
            except ProductImage.DoesNotExist:
                try:
                    add_img_instance(u.pk, main_image_url, is_main=True)
                # img_url is invalid
                except:
                    pass
            
            #continue going through imgs to create instances
            for i in range(28,31):
                try:
                    add_img_instance(u.pk, data[i])    
                except Exception, e:
                    logger.info('No {} Image for {}'.format(headers[i], u))

            logger.info('Added {} to database'.format(u))
                        
            # except Exception, e:
            #     logger.error('Error Saving {} from google into database'.format(u))
            #     logger.error(str(e))
            