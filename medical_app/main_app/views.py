from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from .forms import GeographicalAreaCreateForm, TreatmentsCreateForm
from .models import *


class HomePageView(View):
    """ Start (home) page. """

    template = 'home_page.html'

    def get(self, request):
        return render(request, self.template)


class OrgansListView(ListView):
    """ Page with organs list from DB. """

    model = Organ
    context_object_name = 'organs'
    template_name = 'organs_list.html'


class SymptomsListView(View):
    """ Page with all symptoms from DB. """

    template = 'symptoms_list.html'

    def get(self, request):
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        organs = get_list_or_404(Organ.objects.order_by('name'))
        ctx = {'symptoms': symptoms,
               'organs': organs}
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


class TreatmentsListView(CreateView, ListView):
    """ Page with all treatments from DB. """

    model = Treatment
    object_list = Treatment.objects.all()
    form_class = TreatmentsCreateForm
    template_name = 'treatments_list.html'
    context_object_name = 'treatments'
    success_url = reverse_lazy('treatments_list')


class GeographicalAreaListView(CreateView, ListView):
    """ Page with all geographical areas from DB. """

    model = GeographicalArea
    object_list = GeographicalArea.objects.all()
    form_class = GeographicalAreaCreateForm
    context_object_name = 'areas'
    template_name = 'geographical_areas_list.html'
    success_url = reverse_lazy('geographical_areas_list')

    # def get_ctx(self):
    #     areas = get_list_or_404(GeographicalArea.objects.order_by('area'))
    #     ctx = {'areas': areas}
    #     return ctx
    #
    # def get(self, request):
    #     return render(request, self.template, self.get_ctx())
    #
    # def post(self, request):
    #     geographical_area = request.POST.get('geographical_area')
    #     image = request.FILES.get('image')
    #
    #     if not geographical_area:
    #         return render(request, self.template, self.get_ctx())
    #
    #     if not image:
    #         return render(request, self.template, self.get_ctx())
    #
    #     GeographicalArea.objects.create(
    #         area=geographical_area,
    #         image=image
    #     )
    #
    #     return render(request, self.template, self.get_ctx())


class DiseasesListView(ListView):
    """ Page with all disease from DB. """

    model = Disease
    context_object_name = 'diseases'
    template_name = 'diseases_list.html'


class DiseaseDetailsView(DetailView):
    """ Page with disease's details like description, affected organs, symptoms, treatment. """

    model = Disease
    template_name = 'disease_details.html'

    def get_context_data(self, **kwargs):
        disease = get_object_or_404(Disease, pk=self.kwargs['pk'])
        symptoms_details = DiseaseSymptom.objects.filter(disease=disease).order_by('-symptom_frequency')
        ctx = super().get_context_data(**kwargs)
        ctx["symptoms_details"] = symptoms_details
        return ctx


class SearchDiseaseView(View):
    """ Searching for disease by symptoms and affected organs. """

    template = 'search_disease.html'

    def get(self, request):
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        organs = get_list_or_404(Organ.objects.order_by('name'))
        geographical_areas = get_list_or_404(GeographicalArea.objects.order_by('area'))
        ctx = {'symptoms': symptoms,
               'organs': organs,
               'geographical_areas': geographical_areas}
        return render(request, self.template, ctx)

    def post(self, request):
        symptoms = request.POST.getlist('symptoms')
        organs = request.POST.getlist('affected_organs')
        geographical_areas = request.POST.getlist('geographical_areas')

        if organs:
            try:
                diseases = Disease.objects.filter(affected_organs__in=organs).distinct()
            except:
                raise Http404

        if geographical_areas:
            try:
                diseases = Disease.objects.filter(geographical_area__in=geographical_areas).distinct()
            except:
                raise Http404

        if symptoms:
            try:
                diseases = Disease.objects.filter(symptoms__in=symptoms).distinct()
            except:
                raise Http404

        if not organs and not symptoms and not geographical_areas:
            diseases = Disease.objects.order_by('name')

        ctx = {'diseases': diseases}
        return render(request, 'diseases_list.html', ctx)


class AddNewOrganView(View):
    """ Adding new organ to DB. """
    # model = Organ
    # template_name = 'add_new_organ.html'
    # form_class = OrganCreateForm
    # success_url = reverse_lazy('organs_list')
    template = 'add_new_organ.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name:
            ctx = {'message': 'Name cannot be empty!'}
            return render(request, self.template, ctx)
        if len(name) > 255:
            ctx = {'message': 'Name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)
        if not image:
            ctx = {'message': 'You have to choose a image for new organ!'}
            return render(request, self.template, ctx)

        Organ.objects.create(
            name=name,
            description=description,
            image=image
        )
        return HttpResponseRedirect(reverse('organs_list'))


class AddNewDiseaseView(View):
    """ Adding new disease to DB. """

    template = 'add_new_disease.html'

    def get_ctx(self):
        organs = get_list_or_404(Organ.objects.order_by('name'))
        symptoms = get_list_or_404(Symptom.objects.order_by('name'))
        choices = DiseaseSymptom.SYMPTOM_FREQUENCY_CHOICES
        treatment = Treatment.objects.order_by('treatment')
        geographical_areas = GeographicalArea.objects.order_by('area')
        ctx = {'organs': organs,
               'symptoms': symptoms,
               'symptom_frequency_choices': choices,
               'treatment': treatment,
               'geographical_areas': geographical_areas}
        return ctx

    def get(self, request):
        ctx = self.get_ctx()
        return render(request, self.template, ctx)

    def post(self, request):
        # Try QueryString or Ajax to send post data
        ctx = self.get_ctx()
        name = request.POST.get('name')
        description = request.POST.get('description')
        geographical_area = request.POST.getlist('geographical_areas')
        treatment = request.POST.getlist('treatment')
        affected_organs = request.POST.getlist('affected_organs')
        symptoms = request.POST.getlist('symptoms')
        symptom_frequency = request.POST.getlist('symptom_frequency')
        symptom_frequency = [i for i in symptom_frequency if i != '0']

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
            ctx['message'] = "Choose symptom's frequency!"
            return render(request, self.template, ctx)

        if len(symptom_frequency) != len(symptoms):
            ctx['message'] = "Choose symptoms with correct symptom's frequency!"
            return render(request, self.template, ctx)

        disease = Disease.objects.create(
            name=name,
            description=description
        )

        disease.geographical_area.set(geographical_area)
        disease.treatment.set(treatment)
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
    """ Authorization page with 2 options: login or register. """

    template = 'authorization.html'

    def get(self, request):
        return render(request, self.template)


class LogInView(View):
    """ Login page. """

    template = 'log_in.html'

    def get(self, request):
        return render(request, self.template)


class RegistrationView(View):
    """ Register page. """

    template = 'registration.html'

    def get(self, request):
        return render(request, self.template)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_repeat = request.POST.get('password_repeat')
        medical_license = request.POST.get('license')

        if not first_name:
            ctx = {'message': 'First name cannot be empty!'}
            return render(request, self.template, ctx)
        if len(first_name) > 255:
            ctx = {'message': 'First name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)

        if not last_name:
            ctx = {'message': 'Last name cannot be empty!'}
            return render(request, self.template, ctx)
        if len(last_name) > 255:
            ctx = {'message': 'Last name cannot be longer than 255 characters!'}
            return render(request, self.template, ctx)

        if not email:
            ctx = {'message': 'Email cannot be empty!'}
            return render(request, self.template, ctx)

        if not password:
            ctx = {'message': 'Password cannot be empty!'}
            return render(request, self.template, ctx)
        if not password_repeat:
            ctx = {'message': 'Repeat your password, please!'}
            return render(request, self.template, ctx)
        if password != password_repeat:
            ctx = {'message': 'Passwords are different!'}
            return render(request, self.template, ctx)

        # new_user = User.objects.create_user(
        #     first_name=first_name,
        #     last_name=last_name,
        #     email=email,
        #     password=password,
        #     medical_license=medical_license
        # )

        return HttpResponseRedirect(reverse('home_page'))
