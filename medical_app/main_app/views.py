import re

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.views.generic import View

from .clcrypto import *
from .models import *


class HomePageView(View):
    ''' Start (home) page. '''

    template = 'home_page.html'

    def get(self, request):
        return render(request, self.template)


class OrgansListView(View):
    ''' Page with organs list from DB. '''

    template = 'organs_list.html'

    def get(self, request):
        organs = get_list_or_404(Organ.objects.order_by('name'))
        ctx = {'organs': organs}
        return render(request, self.template, ctx)


class SymptomsListView(View):
    ''' Page with all symptoms from DB. '''

    template = 'symptoms_list.html'

    def get(self, request):
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        ctx = {'symptoms': symptoms}
        return render(request, self.template, ctx)


class DiseasesListView(View):
    ''' Page with all disease from DB. '''

    template = 'diseases_list.html'

    def get(self, request):
        diseases = get_list_or_404(Disease.objects.order_by('name'))
        ctx = {'diseases': diseases}
        return render(request, self.template, ctx)


class DiseaseDetailsView(View):
    ''' Page with disease's details like description, affected organs, symptoms, treatment. '''

    template = 'disease_details.html'

    def get(self, request, **kwargs):
        disease = get_object_or_404(Disease, pk=kwargs['disease_pk'])
        symptoms_details = DiseaseSymptom.objects.filter(disease=disease).order_by('-symptom_frequency')
        ctx = {'disease': disease,
               'symptoms_details': symptoms_details}
        return render(request, self.template, ctx)


class SearchDiseaseView(View):
    ''' Searching for disease by symptoms and affected organs. '''

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
    ''' Adding new organ to DB. '''

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
    ''' Adding new symptom to DB. '''

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
    ''' Adding new disease to DB. '''

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
        # Try QueryString or Ajax to send post data
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
            ctx['message'] = 'Treatment cannot be empty!'
            return render(request, self.template, ctx)

        if not affected_organs:
            ctx['message'] = 'Choose one or more affected organs!'
            return render(request, self.template, ctx)

        if not symptoms:
            ctx['message'] = 'Choose one or more symptoms!'
            return render(request, self.template, ctx)

        if not symptom_frequency:
            symptom_frequency = [0 for _ in range(len(symptoms))]

        if len(symptom_frequency) != len(symptoms):
            ctx['message'] = "Choose symptoms with correct symptom's frequency!"
            return render(request, self.template, ctx)

        disease = Disease.objects.create(
            name=name,
            description=description,
            geographical_area=geographical_area,
            treatment=treatment
        )

        disease.affected_organs.set(affected_organs)

        for i in range(0, len(symptoms)):
            symptom = Symptom.objects.get(pk=symptoms[i])
            DiseaseSymptom.objects.create(
                disease=disease,
                symptom=symptom,
                symptom_frequency=symptom_frequency[i]
            )

        disease.save()
        return HttpResponseRedirect(reverse('diseases_list'))


class AuthorizationView(View):
    ''' Authorization page with 2 options: login or register. '''

    template = 'authorization.html'

    def get(self, request):
        return render(request, self.template)


class LogInView(View):
    ''' Login page. '''

    pass


class RegistrationView(View):
    ''' Register page. '''

    template = 'registration.html'

    def check_email(self, request, email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, email):
            return email
        else:
            ctx = {'message': 'Incorrect email!'}
            return render(request, self.template, ctx)

    def hash_password(self, password, salt=''):
        password = hash_password(password, salt)
        return password

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not first_name:
            ctx = {'message': 'First name cannot be empty!'}
            return render(request, self.template, ctx)
        if not last_name:
            ctx = {'message': 'Last name cannot be empty!'}
            return render(request, self.template, ctx)
        if not email:
            ctx = {'message': 'Email cannot be empty!'}
            return render(request, self.template, ctx)
        if not password:
            ctx = {'message': 'Password cannot be empty!'}
            return render(request, self.template, ctx)

        if len(first_name) > 255:
            ctx = {'message': 'First name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)
        if len(last_name) > 255:
            ctx = {'message': 'Last name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)

        email = self.check_email(request, email)

        if len(password) < 8:
            ctx = {'message': 'Password must be longer than 8 characters!'}
            return render(request, self.template, ctx)
        if len(password) > 20:
            ctx = {'message': 'Password cannot be longer than 20 characters!'}
            return render(request, self.template, ctx)

        for sing in password:
            if sing not in ALPHABET:
                ctx = {'message': 'Password must not contains spaces, special characters, or emoji!'}
                return render(request, self.template, ctx)

        password = self.hash_password(password)

        User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        ctx = {'message': 'Registration completed successfully!'}
        return render(request, self.template, ctx)
