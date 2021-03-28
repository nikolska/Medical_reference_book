from formtools.preview import FormPreview
from formtools.wizard.views import WizardView, SessionWizardView

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, View

from .forms import (
    DiseaseCreateForm, GeographicalAreaCreateForm, OrganCreateForm,
    SymptomCreateForm, TreatmentsCreateForm
)
from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment


User = get_user_model()


class HomePageView(TemplateView):
    """ Start (home) page. """

    template_name = 'home_page.html'


class OrgansListView(ListView):
    """ Page with organs list from DB. """

    model = Organ
    context_object_name = 'organs'
    template_name = 'organs_list.html'


class SymptomsListView(CreateView, ListView):
    """ Page with all symptoms from DB. """

    model = Symptom
    object_list = Symptom.objects.all()
    form_class = SymptomCreateForm
    template_name = 'symptoms_list.html'
    context_object_name = 'symptoms'
    success_url = reverse_lazy('symptoms_list')


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
        """Insert the form into the context dict"""

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


class AddNewOrganView(CreateView):
    """ Adding new organ to DB. """
    model = Organ
    template_name = 'add_new_organ.html'
    form_class = OrganCreateForm
    success_url = reverse_lazy('organs_list')


class DiseaseCreateView(CreateView):
    """Create new disease"""

    model = Disease
    form_class = DiseaseCreateForm
    template_name = 'add_new_disease.html'
    success_url = reverse_lazy('disease_details')

    def get_success_url(self, **kwargs):
        """Return the URL to redirect to after processing a valid form"""
        return reverse("disease_details", kwargs={'pk': self.object.pk})


class AuthorizationView(View):
    """ Authorization page with 2 options: login or register. """

    template = 'authorization.html'

    def get(self, request):
        return render(request, self.template)


class LogInView(FormView):
    """ Login page. """

    template_name = 'log_in.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.login(self.request)
        return super().form_valid(form)


class RegistrationView(View):
    """ Register page. """

    template = 'registration.html'
