
from django.urls import path
from app import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('',views.home,name='home'),

    path('registration/',views.registration,name='registration'),

    path('accounts/login/', views.LoginView, name='login'),

    path('send_otp/', views.Send_Otp, name='send_otp'),

    path('enter_otp/', views.Enter_Otp, name='enter_otp'),

    path('forgot_password/', views.Forgot_Password, name='forgot_password'),

    path('password_reset/', views.Password_Reset, name='password_reset'),

    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('passwordchange/', views.Password_Change,name='passwordchange'),
]
