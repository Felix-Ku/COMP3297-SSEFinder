from django.contrib import admin
from django.urls import path
from CovidDataPortal import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('home/', views.index, name='index'),
    #### Old urls
    # path('LocationAdd/', views.AddLocation, name='AddLocation'),
    # path('LocationData_list/', views.LocationData_list_view, name='LocationData_list'),
    #### New urls
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('Case_records/Create_record/', views.Create_record, name='Create_record'),
    path('Case_records/All_cases/', views.All_cases, name='All_cases'),
    path('Case_records/All_cases_success/', views.All_cases_success, name='All_cases_success'),
    path('Case_records/Case_query/', views.Case_query, name='Case_query'),
    path('Case_records/Create_attendance/', views.Create_attendance, name='Create_attendance'),
    path('SSE_Finder/', views.SSE_Finder, name='SSE_Finder'),
    # path('', views.login, name='login'),
]
