"""property URL Configuration

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
from django.urls import path
from django.conf.urls import url, include
from property_app import views

urlpatterns = [
    url(r'^admin/', views.admin),
    url(r'^language_add/', views.language_add),
    url(r'^language_del/', views.language_del),
    url(r'^env/', views.env),
    url(r'^env_list/', views.env_list),
    url(r'^env_add/', views.env_add),
    url(r'^env_del/', views.env_del),
    url(r'^env_edit/', views.env_edit),
    url(r'^app/', views.app),
    url(r'^app_add/', views.app_add),
    url(r'^app_idc_add/', views.app_idc_add),
    url(r'^app_idc_list/', views.app_idc_list),
    url(r'^app_idc_del/', views.app_idc_del),
    url(r'^app_edit/', views.app_edit),
    url(r'^app_del/', views.app_del),
    url(r'^domain/', views.domain),
    url(r'^domain_add/', views.domain_add),
    url(r'^domain_edit/', views.domain_edit),
    url(r'^domain_del/', views.domain_del),
    url(r'^idc/', views.idc),
    url(r'^idc_all/', views.idc_all),
    url(r'^idc_add/', views.idc_add),
    url(r'^idc_edit/', views.idc_edit),
    url(r'^idc_del/', views.idc_del),
    url(r'^idc_all_add/', views.idc_all_add),
    url(r'^idc_all_del/', views.idc_all_del),
    url(r'^host_list/', views.host_list),
    url(r'^home/', views.home),
]
