from django.contrib import admin

from goods.models import Product, Segment, Style, Category, Subcategory, Material

# class SegmentInline(admin.TabularInline):
# 	model = Segment

# class MaterialInline(admin.TabularInline):
# 	model = Material
# @admin.register(Segment, Style, Category, Subcategory, Material)
# class PersonAdmin(admin.ModelAdmin):
#     pass

class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_select_related = True
	filter_horizontal = ['segment', 'style', 'category', 'subcategory', 'material']

admin.site.register(Product, ProductAdmin)
