from django.contrib import admin

from goods.models import Product, Color, Segment, Style, FurnitureType, ValueTier, Category, Subcategory, Material, ProductImage, Comment

@admin.register(Segment, Style, Color, FurnitureType, ValueTier, Category, Subcategory, Material)
class TagAdmin(admin.ModelAdmin):
	pass


class ProductImageInline(admin.StackedInline):
	model = ProductImage
	fields = (('image','is_main'),)
	verbose_name = 'photo'


class CommentInline(admin.StackedInline):
	model = Comment
	fields = ('product','authuser','message')


class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_display = ['short_name', 'id', 'store', 'current_price', 'original_price', 'is_published','is_sold','is_featured']
	fields = [('short_name', 'is_published','is_sold', 'is_featured'), 'store', 'units',('original_price', 'current_price', 'value_tier'), 
				'pub_date', 'description',('style','color','segment','furnituretype','category','subcategory','material'),
				'width','depth','height','seat_height','diameter','bed_size']
	# filter_horizontal = ['style','segment','category','subcategory','material']
	inlines = [ProductImageInline]
	search_fields = ['short_name', 'long_name','store']
	list_filter = ['store']
	prepopulated_fields = {"current_price": ("original_price",)}

	
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
