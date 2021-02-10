from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import *


class HomePageView(View):
    template = 'home_page.html'

    def get(self, request):
        return render(request, self.template)


class OrgansListView(View):
    template = 'organs_list.html'

    def get(self, request):
        organs = Organ.objects.order_by('name')
        ctx = {'organs': organs}
        return render(request, self.template, ctx)


class SymptomsListView(View):
    template = 'symptoms_list.html'

    def get(self, request):
        symptoms = Symptom.objects.order_by('name')
        ctx = {'symptoms': symptoms}
        return render(request, self.template, ctx)


class DiseasesListView(View):
    template = 'diseases_list.html'

    def get(self, request):
        diseases = Disease.objects.order_by('name')
        ctx = {'diseases': diseases}
        return render(request, self.template, ctx)


class DiseaseDetailsView(View):
    template = 'disease_details.html'

    def get(self, request, **kwargs):
        disease = get_object_or_404(Disease, pk=kwargs['disease_pk'])
        symptoms_details = DiseaseSymptom.objects.filter(disease=disease).order_by('-symptom_frequency')
        ctx = {'disease': disease,
               'symptoms_details': symptoms_details}
        return render(request, self.template, ctx)


class SearchDiseaseView(View):
    pass

