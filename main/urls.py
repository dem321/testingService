from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='idx'),
    path('registration', views.registration, name='reg'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
