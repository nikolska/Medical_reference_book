from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View

from .models import *


class HomePageView(View):
    template = 'home_page.html'

    def get(self, request):
        return render(request, self.template)


class OrgansListView(View):
    template = 'organs_list.html'

    def get(self, request):
        organs = get_list_or_404(Organ.objects.order_by('name'))
        ctx = {'organs': organs}
        return render(request, self.template, ctx)


class SymptomsListView(View):
    template = 'symptoms_list.html'

    def get(self, request):
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        ctx = {'symptoms': symptoms}
        return render(request, self.template, ctx)


class DiseasesListView(View):
    template = 'diseases_list.html'

    def get(self, request):
        diseases = get_list_or_404(Disease.objects.order_by('name'))
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
    template = 'search_disease.html'

    def get(self, request):
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        organs = get_list_or_404(Organ.objects.order_by('name'))
        ctx = {'symptoms': symptoms,
               'organs': organs}
        return render(request, self.template, ctx)

    def post(self, request):
        symptoms = request.POST.getlist('symptoms')
        organs = request.POST.getlist('affected_organs')

        if organs:
            try:
                diseases = Disease.objects.filter(affected_organs__in=organs).distinct()
            except:
                raise Http404

        if symptoms:
            try:
                diseases = Disease.objects.filter(symptoms__in=symptoms).distinct()
            except:
                raise Http404
            
        if not organs and not symptoms:
            diseases = Disease.objects.order_by('name')

        ctx = {'diseases': diseases}
        return render(request, 'diseases_list.html', ctx)

