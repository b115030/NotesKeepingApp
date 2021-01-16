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


urlpatterns =[ 
    path('admin/', admin.site.urls),
    path('notes/', include('notes.urls')),\
    path('account/', include('account.urls')),
    path('label/', label_view.Labels.as_view(), name="label"),
    path('label/<int:pk>', label_view.Labels.as_view(), name="specific-label"),
    path('all-notes/', note_view.AllNotesAPI.as_view(), name="AllNotes"),
]
