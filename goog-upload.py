#!/usr/bin/env python
import requests
email = 'blakesadams@gmail.com'
password = 'Bloopers1423'
import gspread

gc = gspread.login(email, password)
ss = gc.open("Test Trouvaay Upload")
worksheet_list = ss.worksheets()
worksheet = ss.worksheet('Sheet1')

data = worksheet.get_all_values()[1]
price = float(data[1])
print type(price), price