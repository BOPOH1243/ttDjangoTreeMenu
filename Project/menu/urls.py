from django.contrib import admin
from django.urls import path
from menu import views

urlpatterns = [
    path('', views.index, name='index'),
    path('taxonomy/<str:title>/', views.page, name='taxonomy'),
]
