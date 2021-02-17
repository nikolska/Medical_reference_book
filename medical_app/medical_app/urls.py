"""medical_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from main_app.views import *


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('admin/', admin.site.urls),
    path('diseases/', DiseasesListView.as_view(), name='diseases_list'),
    re_path(r'^diseases/(?P<disease_pk>\d+)/$', DiseaseDetailsView.as_view(), name='disease_details'),
    path('diseases/add/', AddNewDiseaseView.as_view(), name='add_disease'),
    path('diseases/search/', SearchDiseaseView.as_view(), name='search_disease'),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('organs/', OrgansListView.as_view(), name='organs_list'),
    path('organs/add/', AddNewOrganView.as_view(), name='add_organ'),
    path('symptoms/', SymptomsListView.as_view(), name='symptoms_list'),
    path('symptoms/add/', AddNewSymptomView.as_view(), name='add_symptom'),
]
