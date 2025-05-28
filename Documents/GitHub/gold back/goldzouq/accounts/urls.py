from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('login_with_mail/',views.login_with_mail,name='login_with_mail'),
    path('mail_otp/<str:email>/', views.mail_otp, name='mail_otp'),
    path('otp_expired/', views.otp_expired_page, name='otp_expired_page'),
    path('login/', views.login_with_otp, name='login_with_otp'),
    path('enter-otp/<str:phone_number>/', views.phone_otp, name='phone_otp'),
    path('register/', views.register, name='register'),
    path('otp-expired/', views.otp_expired_page, name='otp_expired'),
    path('account/', views.account, name='account'),
    path('logout/', views.signout, name='logout'),
]
