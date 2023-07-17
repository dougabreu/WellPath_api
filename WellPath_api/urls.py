"""
URL configuration for WellPath_api project.

The `urlpatterns` list routes URLs to views_well_path. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views_well_path
    1. Add an import:  from my_app import views_well_path
    2. Add a URL to urlpatterns:  path('', views_well_path.home, name='home')
Class-based views_well_path
    1. Add an import:  from other_app.views_well_path import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from well.views_well_path import api


urlpatterns = [
    path('', api.well_api_list),
]
