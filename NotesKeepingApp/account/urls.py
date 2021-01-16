from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration', views.RegisterView.as_view, name="Register"),
    path ('login', views.LoginAPIView.as_view, name="Login"),
    path('logout', views.UserLogoutView.as_view, name= "Logout"),
    path('activate/<uidb64>/<token>',views.VerifyEmail.as_view(), name='activate'),
    path('reset_password', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]