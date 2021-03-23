from django.contrib import admin
from django.urls import path
from CovidDataPortal import views

urlpatterns = [
    path('', views.index, name='index'),
    path('LocationAdd/', views.AddLocation, name='AddLocation'),
    path('LocationData_list/', views.LocationData_list_view, name='LocationData_list'),
    path('Testing/', views.index_test, name='index_test'),
]