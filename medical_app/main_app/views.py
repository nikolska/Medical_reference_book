from formtools.preview import FormPreview
from formtools.wizard.views import WizardView, SessionWizardView

from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import (
    DiseaseCreateForm, DiseaseSearchForm, GeographicalAreaCreateForm,
    OrganCreateForm, SymptomCreateForm, TreatmentsCreateForm, UserCreateForm, UserUpdateForm
)
from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment, User


class AuthorizationView(TemplateView):
    """ Authorization page with 2 options: login or register. """

    template_name = 'authorization.html'


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


class DiseasesListView(ListView):
    """ Page with all disease from DB. """

    model = Disease
    context_object_name = 'diseases'
    template_name = 'diseases_list.html'


class DiseaseSearchView(FormView):
    """ Searching for disease by symptoms and affected organs. """

    model = Disease
    template_name = 'search_disease.html'
    form_class = DiseaseSearchForm

    def post(self, request, *args, **kwargs):
        """Filter DB to search objects and redirect URL with found diseases."""

        symptoms = request.POST.getlist('symptoms')
        organs = request.POST.getlist('affected_organs')
        geographical_area = request.POST.getlist('geographical_area')

        diseases = Disease.objects.all()
        diseases = diseases.filter(affected_organs__in=organs) if organs else diseases
        diseases = diseases.filter(geographical_area__in=geographical_area) if geographical_area else diseases
        diseases = diseases.filter(symptoms__in=symptoms) if symptoms else diseases

        ctx = {'diseases': diseases}
        return render(request, 'diseases_list.html', ctx)


class GeographicalAreaListView(CreateView, ListView):
    """ Page with all geographical areas from DB. """

    model = GeographicalArea
    object_list = GeographicalArea.objects.all()
    form_class = GeographicalAreaCreateForm
    context_object_name = 'areas'
    template_name = 'geographical_areas_list.html'
    success_url = reverse_lazy('geographical_areas_list')


class HomePageView(TemplateView):
    """ Start (home) page. """

    template_name = 'home_page.html'


class OrgansListView(ListView):
    """ Page with organs list from DB. """

    model = Organ
    context_object_name = 'organs'
    template_name = 'organs_list.html'


class OrganCreateView(UserPassesTestMixin, CreateView):
    """ Adding new organ to DB. """
    model = Organ
    template_name = 'add_new_organ.html'
    form_class = OrganCreateForm
    success_url = reverse_lazy('organs_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctors').exists()


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


class SymptomsListView(SuccessMessageMixin, CreateView, ListView):
    """ Page with all symptoms from DB. """

    model = Symptom
    object_list = Symptom.objects.all()
    form_class = SymptomCreateForm
    context_object_name = 'symptoms'
    template_name = 'symptoms_list.html'
    success_message = "New symptom %(name)s successfully created!"
    success_url = reverse_lazy('symptoms_list')


class TreatmentsListView(SuccessMessageMixin, CreateView, ListView):
    """ Page with all treatments from DB. """

    model = Treatment
    object_list = Treatment.objects.all()
    form_class = TreatmentsCreateForm
    context_object_name = 'treatments'
    template_name = 'treatments_list.html'
    success_message = "New treatment %(treatment)s successfully created!"
    success_url = reverse_lazy('treatments_list')


class UserDataUpdateView(PermissionRequiredMixin, UpdateView):
    """Change user's data: first and last name, email."""

    model = User
    form_class = UserUpdateForm
    template_name = 'change_data.html'
    success_url = reverse_lazy('home_page')
    permission_required = 'main_app.change_user'


class UserPasswordUpdateView(PermissionRequiredMixin, PasswordChangeView):
    """Change user's password."""

    template_name = 'change_password.html'
    success_url = reverse_lazy('home_page')
    permission_required = 'main_app.change_user'
