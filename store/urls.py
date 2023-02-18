from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChange, MyPasswordResetForm, MySetPasswordForm
urlpatterns = [
    #path('', views.home),
    path('', views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html' ,form_class=MyPasswordChange, success_url='/passwordchangedone'), name='changepassword'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passchangedone.html'), name='passwordchangedone'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='app/passwordreset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/passwordreset_confirm.html',form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='app/passwordreset_complete.html'), name='password_reset_complete'),
    path('mobile/>', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('topwear/>', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    path('bottomwear/>', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    path('laptop/>', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    #path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('registration/', views.CustomerRegistration, name='customerregistration'),
    # path('registrationdone/', auth_views.PasswordResetCompleteView.as_view(template_name='app/registration_done.html'), name='registration_done'),

    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/' , views.payment_done, name='paymentdone')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
