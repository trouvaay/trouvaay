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
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^productlike/$', views.ProductLike, name='like'),
    url(r'^addtocart/$', views.AddToCart, name='addtocart'),
    url(r'^canreserve/$', views.can_reserve, name='can_reserve'),
    url(r'^reservecallback/$', views.ReserveCallbackView.as_view(), name='reserve_callback'),

    # Unused Cart Feature #
    # url(r'^cart/$', views.CartView.as_view(), name='cart'),
    # url(r'^removefromcart/$', views.RemoveFromCart, name='removefromcart'),
    # url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    # url(r'^checkoutcallback/$', views.CartCheckoutCallbackView.as_view(), name='checkoutcallback'),
)
