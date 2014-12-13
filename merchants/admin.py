from django.contrib import admin
from merchants.models import Retailer, Store, Shipper


class ShipperInline(admin.TabularInline):
    model = Store.shipper.through


class StoreAdmin(admin.ModelAdmin):
	model = Store
	extra = 1
	fields = ['retailer','store_num', 'street','street2','city',
			'state','zipcd','description']
	list_select_related = True
	inline = [ShipperInline]
	exclude = ['shipper']
# 	list_select_related = True

admin.site.register(Store, StoreAdmin)