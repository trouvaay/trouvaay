from django.contrib import admin

from goods.models import Product, Segment, Style, Category, Subcategory, Material, ProductImage, Comment


# class SegmentInline(admin.TabularInline):
# 	model = Segment

# class MaterialInline(admin.TabularInline):
# 	model = Material

@admin.register(Segment, Style, Category, Subcategory, Material)
class TagAdmin(admin.ModelAdmin):
	pass

class ProductImageInline(admin.StackedInline):
	model = ProductImage
	fields = (('name','image','is_main'),)
	verbose_name = 'photo'

class CommentInline(admin.StackedInline):
	model = Comment
	fields = ('product','authuser','message')


class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_display = ['short_name', 'id', 'store', 'current_price', 'original_price', 'is_published']
	fields = [('short_name', 'is_published'), 'store', 'units',('original_price', 'current_price'), 
				'pub_date', ('style','segment','category','subcategory','material')]
	# filter_horizontal = ['style','segment','category','subcategory','material']
	inlines = [ProductImageInline]
	search_fields = ['short_name', 'long_name','store']
	list_filter = ['store']

	

admin.site.register(Product, ProductAdmin)

