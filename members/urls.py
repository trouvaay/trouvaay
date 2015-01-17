from django.conf.urls import patterns, include, url
from members import views
from members.forms import CustomAuthenticationForm


urlpatterns = patterns('',
    url(r'^account/(?P<pk>\d+)$', views.ClosetView.as_view(), name='closet'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'members/auth/login.html', 'authentication_form' : CustomAuthenticationForm}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    #Needs to be updated implemented with registration/signup modal
    # url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^productlike/$', views.ProductLike, name='like'),
    url(r'^cart/$', views.CartView.as_view(), name='cart'),
    url(r'^addtocart/$', views.AddToCart, name='addtocart'),
    url(r'^removefromcart/$', views.RemoveFromCart, name='removefromcart'),
    url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    url(r'^checkoutcallback/$', views.CartCheckoutCallbackView.as_view(), name='checkoutcallback'),
    url(r'^review/$', views.ReviewView.as_view(), name='review'),
    url(r'^payment/$', views.SubmitCustomerPayment, name='payment'),
)