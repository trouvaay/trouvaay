#!/usr/bin/env python
# from goods.models import Product
import requests
email = 'blakesadams@gmail.com'
password = 'Bloopers1423'
import gspread

gc = gspread.login(email, password)
ss = gc.open("Product Master List")
worksheet_list = ss.worksheets()
worksheet = ss.worksheet('Test_upload')

data = worksheet.row_values(2)
