from django.conf.urls import url
from django.urls import path, include
# from .api import RegisterApi
from . import views
from django.contrib.auth import views as auth_views

# urlpatterns = [
#       path('api/register', RegisterApi.as_view()),
#       path('signup/', views.usersignup, name='signup'),
#       url('activate/', views.activate_account, name='activate'),
# ]

urlpatterns = [
    path('registration', views.user_registeration, name="Register"),
    path ('login', views.user_login, name="Login"),
    path('logout', views.user_logout, name= "Logout"),
    path('activate/<uidb64>/<token>',views.VerificationView.as_view(), name='activate'),
    path('reset_password', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]