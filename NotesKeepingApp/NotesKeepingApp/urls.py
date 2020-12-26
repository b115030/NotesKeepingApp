"""NotesKeepingApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account import views
from rest_framework import routers
from notes import views as note_view
from Label import views as label_view

# router = routers.DefaultRouter()
# router.register('users', views.UserDetailsCrud)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('account/', include('account.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    # path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    # path('login/', views.LoginAPIView.as_view()),
    # path('register/', views.RegisterView.as_view()),

    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
    #      name="request-reset-email"),
    # path('password-reset/<uidb64>/<token>/',
    #      views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
    #      name='password-reset-complete')
    # path('accounts/', include('account.urls')),
    # path('signup/', views.signup, name="signup"),  
    # path('activate/<uidb64>/<token>/',views.VerificationView, name='activate'),
    # urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('create-note/', note_view.NotesAPI.as_view(), name="AddNote"),
    path('note/<int:pk>', note_view.NotesAPI.as_view(), name='UpdateNote'),
    path('label/', label_view.Labels.as_view(), name="label"),
    path('label/<int:pk>', label_view.Labels.as_view()),
]
