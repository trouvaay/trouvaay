from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from members.models import AuthUser, AuthUserActivity, AuthOrder, \
    PromotionOffer, Redemption, Join, AuthOrder, Reservation, Purchase, OrderAddress
from django import forms


class CustomUserCreationForm(UserCreationForm):
    """ A form for creating new users. Includes all the required fields, plus a repeated password. """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # emove usrname#
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta(UserCreationForm.Meta):
        model = AuthUser
        fields = ('email', 'is_merchant')


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="password",
                                         help_text="""Raw passwords are not stored, so there is no way to see this
                                         user's password, but you can change the password using <a href=\"password/\">
                                         this form</a>.""")

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta(UserChangeForm.Meta):
        model = AuthUser
        fields = ('email', 'is_merchant')  # May want to reduce fields


    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class AuthUserActivityInline(admin.TabularInline):
    model = AuthUserActivity



class AuthUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'is_merchant', 'is_admin', 'is_superuser',)
    list_filter = ('is_admin', 'is_merchant')

    # change list
    fieldsets = (
        (None, {'fields': ('email', 'password', ('first_name', 'last_name'), ('is_merchant',
                           'is_active'))}),
        ('Permissions', {'fields': (('is_superuser', 'is_admin'),)}),
    )

    # add list
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'is_merchant', 'password1', 'password2')}),
    )
    inlines = [AuthUserActivityInline]
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class OrderAddressInline(admin.TabularInline):
    model = OrderAddress


class AuthOrderAdmin(admin.ModelAdmin):
    model = AuthOrder
    list_display = ('authuser', 'product', 'order_type', 'created_at', 'updated_at', 'converted_from_reservation')
    inlines = (OrderAddressInline,)


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ('authuser', 'order', 'taxes', 'original_price', 'transaction_price')


class ReservationAdmin(admin.ModelAdmin):
    model = Reservation
    list_display = ('authuser', 'order', 'reservation_price', 'is_active', 'reservation_expiration')


class PromotionOfferAdmin(admin.ModelAdmin):
    model = PromotionOffer
    list_display = ('name',
                    'is_active',
                    'offer_type',
                    'start_time',
                    'end_time',
                    'is_code_required',
                    'code',
                    'is_discount',
                    'discount_fixed_amount',
                    'discount_percent',
                    'discount_limit'
                    )


class RedemptionAdmin(admin.ModelAdmin):
    model = Redemption
    list_display = ('offer', 'authuser', 'order', 'total_before_discount', 'discount_amount', 'timestamp')


class JoinAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'friend', 'timestamp', 'updated']
    class Meta:
        model = Join


admin.site.register(AuthOrder, AuthOrderAdmin)
admin.site.register(AuthUser, AuthUserAdmin)
admin.site.register(AuthUserActivity)
admin.site.register(Join, JoinAdmin)
admin.site.register(PromotionOffer, PromotionOfferAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Redemption, RedemptionAdmin)
admin.site.register(Reservation, ReservationAdmin)
