from django.conf.urls import patterns, include, url
from members import views
from members.forms import CustomAuthenticationForm, RegistrationForm


urlpatterns = patterns('',
    # url(r'^account/(?P<pk>\d+)$', views.ProfileView.as_view(), name='closet'),
    url(r'^login/$', 'django.contrib.auth.views.login', 
        {'template_name': 'members/auth/login.html', 
         'authentication_form' : CustomAuthenticationForm,
         
         # the foolowing unbound instances of forms are needed
         # only for rendering of the template by login 'GET' 
         # the actual login 'POST' will be using authentication_form 
         # from above
         'extra_context': {'login_form': CustomAuthenticationForm(),
                           'signup_form': RegistrationForm()}         
         }, 
        name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^signup/$', views.SignupView.as_view(), name='signup'),
    url(r'^productlike/$', views.ProductLike, name='like'),
    url(r'^addtocart/$', views.AddToCart, name='addtocart'),
    url(r'^reservecallback/$', views.ReserveCallbackView.as_view(), name='reserve_callback'),

    # Unused Cart Feature #
    # url(r'^cart/$', views.CartView.as_view(), name='cart'),
    # url(r'^removefromcart/$', views.RemoveFromCart, name='removefromcart'),
    # url(r'^checkout/$', views.CheckoutView.as_view(), name='checkout'),
    # url(r'^checkoutcallback/$', views.CartCheckoutCallbackView.as_view(), name='checkoutcallback'),
)