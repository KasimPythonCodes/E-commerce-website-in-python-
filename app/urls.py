from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views 
from .forms import LoginForm ,UserChangedPasswordForm ,MyPasswordResetForm ,MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view() , name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view() , name='product-detail'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('registration/' , views.CutomerRegistrationView.as_view() , name='customerregistration'),
    path('profile/', views.ProfileViews.as_view(), name='profile'),
    path('cart/', views.show_cart , name='showcart'),
    path('pluscart/', views.plus_cart , name='pluscart'),
    path('minuscart/', views.minus_cart , name='minuscart'),
    path('removecart/', views.remove_cart , name='removecart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),


    path('buy/', views.buy_now, name='buy-now'), 
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),



    path('accounts/login/' , auth_views.LoginView.as_view(template_name='login.html' , form_class=LoginForm) , name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='passwordchangeform.html' ,
    form_class=UserChangedPasswordForm , success_url='/passwordchangedone/'), name='changepassword'),
    path('passwordchangedone/' , auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/' , auth_views.PasswordResetView.as_view(template_name='password_reset.html' , 
    form_class=MyPasswordResetForm) ,name='password_reset'),
    path('password-reset/done/' , auth_views.PasswordResetView.as_view(template_name='password_reset_done.html' ) ,name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/' , 
    auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_done_confirm.html',
    form_class=MySetPasswordForm ) ,name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html' ) ,name='password_reset_complete'),


    


] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)



