from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.signin, name='login'),
    path('logout', views.signout, name='logout'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

]
