"""CovidData URL Configuration

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
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
import django.contrib.auth.views as auth_view
from CovidDataPortal import views

urlpatterns = [
    url('admin/', admin.site.urls),
    url('login/', auth_view.LoginView, {'template_name': 'login.html'}, name='login'),
    url('logout/', auth_view.LogoutView, {'template_name': 'logout.html'}, name='logout'),
    url('', views.home, name='home'),
    path('CovidDataPortal/', include('CovidDataPortal.urls'), name='home'),
    # path('', RedirectView.as_view(url='/CovidDataPortal/')),
    # path('accounts/', include('django.contrib.auth.urls')) #forloginauthentication
    # #path('', TemplateView.as_view(template_name='base.html')), # new

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
