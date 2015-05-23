from django.conf.urls import patterns, include, url
from members import views
from members.forms import CustomAuthenticationForm, RegistrationForm


urlpatterns = patterns('',
    # url(r'^account/(?P<pk>\d+)$', views.ProfileView.as_view(), name='closet'),
    url(r'^login/$', views.custom_login,
        {'template_name': 'members/auth/login.html',
         'authentication_form' : CustomAuthenticationForm,
        },
        name='login'),
    url(r'^loginfb/$', views.custom_login,
        {'template_name': 'members/auth/login.html',
         'authentication_form' : CustomAuthenticationForm,
         'is_missing_email': True
        },
        name='fb_login_missing_email'),
    url(r'^ajaxlogin/$', views.AjaxLoginView.as_view(), name='ajax_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^member/$', views.ProfileView.as_view(), name='profile'),
    url(r'^productlike/$', views.ProductLike, name='like'),
    url(r'^canreserve/$', views.can_reserve, name='can_reserve'),
    url(r'^reserve/(?P<pk>\d+)/$', views.ReserveView.as_view(), name='reserve'),
    url(r'^buy/$', views.BuyView.as_view(), name='buy'),
    url(r'^offer/$', views.BuyView.as_view(), name='offer', kwargs={'is_offer': True}),
    url(r'^cancel/$', views.CancelReserve, name='cancel_reserve'),
    url(r'^referralsignup/$', views.ReferralSignup.as_view(), name='referral_signup'),
    url(r'^referralinfo/$', views.ReferralInfo.as_view(), name='referral_info'),
    url(r'^postcheckoutupdate/$', views.PostCheckoutUpdate.as_view(), name='post_checkout_update'),
    url(r'^opt-out/$', views.OptoutView.as_view(), name='opt-out'),

    # Unused Cart Feature #
    # url(r'^addtocart/$', views.AddToCart, name='addtocart'),
    # url(r'^cart/$', views.CartView.as_view(), name='cart'),
    # url(r'^removefromcart/$', views.RemoveFromCart, name='removefromcart'),
    # url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    # url(r'^checkoutcallback/$', views.CartCheckoutCallbackView.as_view(), name='checkoutcallback'),
)
