from django.contrib import admin
from members.models import AuthUserOrderItem
from goods.models import Product, Color, Segment, Style, FurnitureType, ValueTier, Category, Subcategory, Material, ProductImage


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


class AuthUserOrderItemInline(admin.TabularInline):
    model = AuthUserOrderItem


class ProductImageAdmin(CustomAdmin):
    model = ProductImage
    list_display = ['image', 'is_main']


class ProductAdmin(CustomAdmin):
    model = Product

    list_display = ['short_name', 'id', 'first_image', 'store', 'click_count', 'is_published', 'is_featured', 'is_reserved', 'is_sold', 'current_price', 'added_date', 'pub_date', 'is_landing', 'is_featured',]

    fields = [('short_name', 'is_published', 'is_sold', 'is_featured'), ('store', 'has_trial', 'units'),('original_price', 'current_price'), 
                'pub_date', 'description',('color', 'color_description'),('style', 'segment', 'furnituretype', 'category', 'subcategory', 'material'),
                'width', 'depth', 'height', 'seat_height', 'diameter', 'bed_size']
    inlines = [ProductImageInline, AuthUserOrderItemInline]

    search_fields = ['short_name', 'id']
    list_filter = ['store', 'is_published', 'furnituretype', 'is_landing']

    list_editable = ['current_price', 'is_published','is_landing', 'is_reserved', 'is_sold', 'is_featured', 'pub_date']
    
    prepopulated_fields = {"current_price": ("original_price",)}

    def first_image(self, obj):
        try:
            url = obj.productimage_set.first().image.build_url()
            return '<img src={} style="width: 100px"/>'.format(url)
        except:
            return None

    def neighborhood(self, obj):
        return obj.store.neighborhood
    
    first_image.allow_tags = True

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
