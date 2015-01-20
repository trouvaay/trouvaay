from django.contrib import admin
from merchants.models import Retailer, Store, Shipper, RetailerImage


class ShipperAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']

class RetailerImageInline(admin.StackedInline):
	model = RetailerImage
	fields = (('image','is_main'),)
	verbose_name = 'photo'

class RetailerAdmin(admin.ModelAdmin):
    list_display = ['legal_name', 'owner', 'website']
    inlines = [RetailerImageInline]

class StoreAdmin(admin.ModelAdmin):
	model = Store
	extra = 1
	list_display = ['street', 'retailer', 'store_num', 'city', 'is_featured']
	
	fieldsets = (
		(None, {'fields': ('retailer','is_featured', 'store_num','has_returns')}),
		('Location', {'fields': (('lat', 'lng'),('street', 'street2'),('city',
			'state','zipcd'))}),
		(None, {'fields': ('description',)}),
		(None, {'classes': ('collapse',),
				'fields': ('shipper',)}
		)
	)
	list_select_related = True
	list_editable =['is_featured']
	
admin.site.register(Store, StoreAdmin)
admin.site.register(Retailer, RetailerAdmin)
admin.site.register(Shipper, ShipperAdmin)

