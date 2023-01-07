from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, PasswordResetForm, SetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>/',
         views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='show-cart'),
    path('pluscart/', views.plus_cart, name='plus-cart'),
    path('minuscart/', views.minus_cart, name='minus-cart'),
    path('removecart/', views.remove_cart, name='remove-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',
         authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(
        template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url="/passwordchangedone/"), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(
         template_name='app/passwordchangedoneview.html'), name='passwordchangedone'),
# first step

    path('passwordreset/', auth_views.PasswordResetView.as_view(
         template_name='app/passwordreset.html',form_class=PasswordResetForm), name='passwordreset'),
# second step

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
         template_name='app/passwordresetdone.html'), name='password_reset_done'),
# third step

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
         template_name='app/passwordresetconfirm.html',form_class=SetPasswordForm), name='password_reset_confirm'),
# fourth step

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='app/passwordresetcomplete.html'), name='password_reset_complete'),

    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.paymentdone, name='paymentdone')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # image configuration
