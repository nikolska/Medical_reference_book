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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from main_app.views import (
    AuthorizationView, ContactView, DiseaseCreateView, DiseaseDetailsView,
    DiseasesListView, DiseaseSearchView, GeographicalAreaListView,
    HomePageView, OrganCreateView, OrgansListView, RegistrationView,
    SymptomsListView, TreatmentsListView, UserDataUpdateView, UserPasswordUpdateView
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('admin/', admin.site.urls, name='admin'),
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('contact-us/', ContactView.as_view(), name='contact_page'),
    re_path(r'^data-change/(?P<pk>\d+)/$', UserDataUpdateView.as_view(), name='change_data'),
    path('diseases/', DiseasesListView.as_view(), name='diseases_list'),
    re_path(r'^diseases/(?P<pk>\d+)/$', DiseaseDetailsView.as_view(), name='disease_details'),
    path('diseases/add/', DiseaseCreateView.as_view(), name='add_disease'),
    path('diseases/search/', DiseaseSearchView.as_view(), name='search_disease'),
    path('geographical-areas/', GeographicalAreaListView.as_view(), name='geographical_areas_list'),
    path('login/', LoginView.as_view(template_name='log_in.html'), name='log_in'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('organs/', OrgansListView.as_view(), name='organs_list'),
    path('organs/add/', OrganCreateView.as_view(), name='add_organ'),
    re_path(r'^password-change/(?P<pk>\d+)/$', UserPasswordUpdateView.as_view(), name='change_password'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('symptoms/', SymptomsListView.as_view(), name='symptoms_list'),
    path('treatments/', TreatmentsListView.as_view(), name='treatments_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
