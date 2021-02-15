from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template.loader import render_to_string
from django.urls import reverse
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


class AddNewOrganView(View):
    template = 'add_new_organ.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')

        if not name:
            ctx = {'message': 'Name cannot be empty!'}
            return render(request, self.template, ctx)
        if len(name) > 255:
            ctx = {'message': 'Name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)

        Organ.objects.create(
            name=name,
            description=description
        )
        return HttpResponseRedirect(reverse('organs_list'))


class AddNewSymptomView(View):
    template = 'add_new_symptom.html'

    def get(self, request):
        organs = get_list_or_404(Organ.objects.order_by('name'))
        ctx = {'organs': organs}
        return render(request, self.template, ctx)

    def post(self, request):
        name = request.POST.get('name')
        affected_organ = request.POST.get('affected_organ')

        if not name:
            ctx = {'message': 'Name cannot be empty!'}
            return render(request, self.template, ctx)
        if len(name) > 255:
            ctx = {'message': 'Name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)

        Symptom.objects.create(
            name=name,
            affected_organ=Organ.objects.get(pk=affected_organ)
        )
        return HttpResponseRedirect(reverse('symptoms_list'))


class AddNewDiseaseView(View):
    template = 'add_new_disease.html'

    def get_ctx(self):
        organs = get_list_or_404(Organ.objects.order_by('name'))
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        choices = DiseaseSymptom.SYMPTOM_FREQUENCY_CHOICES
        ctx = {'organs': organs,
               'symptoms': symptoms,
               'symptom_frequency_choices': choices}
        return ctx

    def get(self, request):
        ctx = self.get_ctx()
        return render(request, self.template, ctx)

    def post(self, request):
        ctx = self.get_ctx()
        name = request.POST.get('name')
        description = request.POST.get('description')
        geographical_area = request.POST.get('geographical_area')
        treatment = request.POST.get('treatment')
        affected_organs = request.POST.getlist('affected_organs')
        symptoms = request.POST.getlist('symptoms')
        symptom_frequency = request.POST.getlist('symptom_frequency')

        if not name:
            ctx['message'] = 'Name cannot be empty!'
            return render(request, self.template, ctx)
        if len(name) > 255:
            ctx['message'] = 'Name cannot be longer than 255 characters!'
            return render(request, self.template, ctx)

        if not description:
            ctx['message'] = 'Description cannot be empty!'
            return render(request, self.template, ctx)

        if not geographical_area:
            ctx['message'] = 'Geographical area cannot be empty!'
            return render(request, self.template, ctx)

        if not treatment:
            ctx = {'message': 'Treatment cannot be empty!'}
            return render(request, self.template, ctx)

        if not affected_organs:
            ctx = {'message': 'Choose one or more affected organs!'}
            return render(request, self.template, ctx)

        if not symptoms:
            ctx = {'message': 'Choose one or more symptoms!'}
            return render(request, self.template, ctx)

        disease = Disease.objects.create(
            name=name,
            description=description,
            geographical_area=geographical_area,
            treatment=treatment,
        )

        if affected_organs:
            disease.affected_organs.set(affected_organs)

        # if symptoms:
        #     for symptom in symptoms:
        #         symptom = DiseaseSymptom.objects.create(
        #             disease=disease,
        #             symptom=Symptom.objects.get(pk=symptom),
        #             symptom_frequency=symptom_frequency
        #         )
        #         disease.symptoms.set = DiseaseSymptom.objects.get(pk=symptom.pk)

        disease.save()
        return HttpResponseRedirect(reverse('diseases_list'))
