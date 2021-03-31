from formtools.preview import FormPreview
from formtools.wizard.views import WizardView, SessionWizardView

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView

from .forms import (
    DiseaseCreateForm, DiseaseSearchForm, GeographicalAreaCreateForm,
    OrganCreateForm, SymptomCreateForm, TreatmentsCreateForm, UserCreateForm
)
from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment, User


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


class SearchDiseaseView(FormView, ListView):
    """ Searching for disease by symptoms and affected organs. """

    model = Disease
    template_name = 'search_disease.html'
    form_class = DiseaseSearchForm
    success_url = reverse_lazy('search_disease')

    def get_queryset(self):
        """Return the list of items for this view"""

        symptoms = self.request.GET.getlist('symptoms')
        affected_organs = self.request.GET.getlist('affected_organs')
        geographical_area = self.request.GET.getlist('geographical_area')

        object_list = Disease.objects.all()
        data = symptoms, affected_organs, geographical_area

        if any(data):
            symptoms = symptoms if symptoms else Symptom.objects.all()
            affected_organs = affected_organs if affected_organs else Organ.objects.all()
            geographical_area = geographical_area if geographical_area else GeographicalArea.objects.all()

            diseases = Disease.objects.filter(
                symptoms__in=symptoms,
                affected_organs__in=affected_organs,
                geographical_area__in=geographical_area
            ).distinct()

            object_list = diseases
            return object_list
        else:
            return object_list


class OrganCreateView(UserPassesTestMixin, CreateView):
    """ Adding new organ to DB. """
    model = Organ
    template_name = 'add_new_organ.html'
    form_class = OrganCreateForm
    success_url = reverse_lazy('organs_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctors').exists()


class DiseaseCreateView(UserPassesTestMixin, CreateView):
    """Create new disease"""

    model = Disease
    form_class = DiseaseCreateForm
    template_name = 'add_new_disease.html'
    success_url = reverse_lazy('disease_details')

    def get_success_url(self, **kwargs):
        """Return the URL to redirect to after processing a valid form"""
        return reverse("disease_details", kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.request.user.groups.filter(name='Doctors').exists()


class AuthorizationView(TemplateView):
    """ Authorization page with 2 options: login or register. """

    template_name = 'authorization.html'


class RegistrationView(FormView):
    """ Registration page. """

    model = User
    form_class = UserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('log_in')

    def form_valid(self, form):
        """If the form is valid, register the user."""
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        medical_license = form.cleaned_data['medical_license']

        doctors = Group.objects.get(name='Doctors')
        patients = Group.objects.get(name='Patients')
        permission = Permission.objects.get(name='Can change user')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            medical_license=medical_license
        )

        if medical_license is True:
            user.groups.add(doctors)
        else:
            user.groups.add(patients)

        user.set_password(password)
        user.user_permissions.add(permission)
        user.save()
        return HttpResponseRedirect(self.get_success_url())


class UserPasswordUpdateView(PermissionRequiredMixin, PasswordChangeView):
    """Change user's password."""

    template_name = 'change_password.html'
    success_url = reverse_lazy('home_page')
    permission_required = 'main_app.change_user'

