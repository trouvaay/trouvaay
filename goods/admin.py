from django.contrib import admin
from members.models import AuthOrder
from goods.models import Product, Color, Segment, Style, FurnitureType, ValueTier, Category, Subcategory, Material, ProductImage
from import_export.admin import ExportMixin
from django.conf import settings


class CustomAdmin(admin.ModelAdmin):
    """
    customized admin class.
    superuser can delete objects, but admin user(is_admin) is not allowed
    """
    def get_actions(self, request):
        actions = super(CustomAdmin, self).get_actions(request)
        if not request.user.is_superuser and request.user.is_admin:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        elif request.user.is_admin:
            return False
        return True


admin.site.register(Segment, CustomAdmin)
admin.site.register(Style, CustomAdmin)
admin.site.register(Color, CustomAdmin)
admin.site.register(FurnitureType, CustomAdmin)
admin.site.register(ValueTier, CustomAdmin)
admin.site.register(Category, CustomAdmin)
admin.site.register(Material, CustomAdmin)


class TagAdmin(admin.ModelAdmin):
    pass


class SubcategoryAdmin(CustomAdmin):
    list_display = ['select', 'trial_product']
    list_editable = ['trial_product']

admin.site.register(Subcategory, SubcategoryAdmin)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    fields = (('image', 'is_main'),)
    verbose_name = 'photo'


class ProductInline(admin.TabularInline):
    model = Product


class AuthOrderInline(admin.TabularInline):
    model = AuthOrder


class ProductImageAdmin(CustomAdmin):
    model = ProductImage
    list_display = ['image', 'is_main']


class ProductAdmin(ExportMixin, CustomAdmin):
    model = Product

    list_display = ['short_name', 'id', 'first_image', 'description', 'store', 'added_date', 'is_published', 'pub_date', 'is_sold', 'sold_date', 'list_price','current_price', 'hours_left','display_score', 'click_count']

    fields = [('short_name', 'is_published', 'is_sold', 'is_featured'), ('store', 'units'),('original_price', 'current_price'), 
            'description',('color', 'color_description'),('style', 'segment', 'furnituretype', 'category', 'subcategory', 'material'),
                'width', 'depth', 'height', 'seat_height', 'diameter', 'bed_size']
    inlines = [ProductImageInline, AuthOrderInline]

    search_fields = ['short_name', 'id']
    list_filter = ['store', 'is_sold', 'is_published', 'the_hunt', 'furnituretype']

    list_editable = ['current_price', 'is_published', 'pub_date', 'description', 'is_sold']
    
    prepopulated_fields = {"current_price": ("original_price",)}

    ordering = ('-sold_date', '-pub_date')

    def first_image(self, obj):
        try:
            url = obj.productimage_set.first().image.build_url()
            print(url)
            return '<a href=http://{}{} target="_blank"><img src={} style="width: 100px"/></a>'.format(settings.SITE_DOMAIN, obj.get_absolute_url(), url)
        except:
            return None


    def neighborhood(self, obj):
        return obj.store.neighborhood
    
    first_image.allow_tags = True
    

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
