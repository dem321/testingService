from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('', views.index, name='idx'),
    path('registration', views.registration, name='reg'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('test/<int:test_id>/', views.test_view, name='test_description'),
    path('test/<int:test_id>/<int:question_order>', views.question_view, name='question'),
    path('test/<int:test_id>/summary', views.summary, name='summary')
]
