from django.contrib import admin
from merchants.models import Retailer, Store, Shipper


class ShipperInline(admin.TabularInline):
    model = Shipper

class StoreAdmin(admin.ModelAdmin):
	model = Store
	extra = 1
	list_display = ['street', 'retailer', 'store_num', 'city']
	
	fieldsets = (
		(None, {'fields': ('retailer','store_num')}),
		('Location', {'fields': ('street', 'street2','city',
			'state','zipcd')}),
		(None, {'fields': ('description',)}),
		(None, {'classes': ('collapse',),
				'fields': ('shipper',)}
		)
	)
	list_select_related = True
	

# 	list_select_related = True

admin.site.register(Store, StoreAdmin)
admin.site.register(Retailer)
admin.site.register(Shipper)

