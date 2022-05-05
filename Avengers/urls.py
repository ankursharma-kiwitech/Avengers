from django.contrib import admin
from django.urls import path, include
from . import views
from django.views import View

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.register.as_view(), name='signup'),
    path('login', views.Login.as_view(),name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('activate/<uid>/<token>', views.Activate, name='activate'),
]
