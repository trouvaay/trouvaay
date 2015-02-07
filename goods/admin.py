from django.contrib import admin
from members.models import AuthUserOrderItem
from goods.models import Product, Color, Segment, Style, FurnitureType, ValueTier, Category, Subcategory, Material, ProductImage


@admin.register(Segment, Style, Color, FurnitureType, ValueTier, Category, Material)
class TagAdmin(admin.ModelAdmin):
    pass


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ['select', 'trial_product']
    list_editable = ['trial_product']

admin.site.register(Subcategory, SubcategoryAdmin)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    fields = (('image', 'is_main'),)
    verbose_name = 'photo'


class ProductInline(admin.TabularInline):
    model = Product


class AuthUserOrderItemInline(admin.TabularInline):
    model = AuthUserOrderItem


class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ['short_name', 'store', 'description', 'is_published', 'is_featured', 'is_sold', 'current_price', 'added_date', 'pub_date']

    fields = [('short_name', 'is_published', 'is_sold', 'is_featured'), ('store', 'has_trial', 'units'),('original_price', 'current_price'), 
                'pub_date', 'description',('color', 'color_description'),('style', 'segment', 'furnituretype', 'category', 'subcategory', 'material'),
                'width', 'depth', 'height', 'seat_height', 'diameter', 'bed_size']
    inlines = [ProductImageInline, AuthUserOrderItemInline]

    search_fields = ['short_name', 'long_name', 'store']
    list_filter = ['store', 'is_published']

    list_editable = ['current_price', 'is_published', 'is_sold', 'is_featured', 'pub_date']
    
    prepopulated_fields = {"current_price": ("original_price",)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
