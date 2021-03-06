from formtools.wizard.views import SessionWizardView

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import mail_admins, send_mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, TemplateView, UpdateView

from .forms import (
    ContactForm, DiseaseCreateForm, DiseaseFormSet, DiseaseSearchForm, 
    GeographicalAreaCreateForm, OrganCreateForm, SymptomCreateForm, 
    TreatmentsCreateForm, UserCreateForm, UserUpdateForm
)
from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment, User
from medical_app.settings import EMAIL_HOST_USER


class AuthorizationView(TemplateView):
    """ Authorization page with 2 options: login or register. """

    template_name = 'authorization.html'


class ContactView(FormView):
    """User can send the message for admin."""

    form_class = ContactForm
    template_name = 'contact_page.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        """If the form is valid, send users's message and redirect to success URL."""
        
        if self.request.user.id is not None:
            sender = self.request.user.full_name
            sender_email = self.request.user.email
        else:
            sender = form.cleaned_data['sender']
            sender_email = form.cleaned_data['sender_email']
        
        message = form.cleaned_data['message_text']

        subject = f'Message from {sender}, {sender_email}'
        
        mail_admins(subject, message, fail_silently=False)
        
        messages.success(self.request, 'Your message successfully sent!')

        return HttpResponseRedirect(self.get_success_url())


class DiseaseCreateView(SuccessMessageMixin, UserPassesTestMixin, SessionWizardView):
    """Create new disease"""

    template_name = "add_new_disease.html"
    form_list = [DiseaseCreateForm, DiseaseFormSet]

    def process_form_data(self, form_list):
        for form in form_list:
            if form.is_valid():
                form_data = self.get_all_cleaned_data()
                formset = form_data['formset-1']
                
                disease = Disease.objects.create(
                    name=form_data['name'],
                    description=form_data['description']
                )

                disease.affected_organs.set(form_data['affected_organs'])
                disease.geographical_area.set(form_data['geographical_area'])
                disease.treatment.set(form_data['treatment'])
                disease.save()

                for i in range(len(formset)):
                    try: 
                        symptom = Symptom.objects.get(name=formset[i]['symptom'])
                        DiseaseSymptom.objects.create(
                            disease=disease,
                            symptom=symptom,
                            symptom_frequency=formset[i]['symptom_frequency']
                        )
                    except KeyError:
                        return form_data

                return form_data

    def done(self, form_list, **kwargs):
        if self.request.method == 'POST':
            self.process_form_data(form_list)
            disease = self.process_form_data(form_list)['name']
            messages.success(self.request, f'New disease {disease} successfully created!')
        return HttpResponseRedirect(reverse('diseases_list'))
    
    def test_func(self):
        return self.request.user.groups.filter(name='Doctors').exists() or self.request.user.is_superuser


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
        # all_world = True if request.POST.get('all_areas') == 'on' else False
        # all_areas_form_db = GeographicalArea.objects.all()
        # all_areas = [item.pk for item in all_areas_form_db] 

        diseases = Disease.objects.all()
        diseases = diseases.filter(affected_organs__in=organs).distinct() if organs else diseases
        diseases = diseases.filter(symptoms__in=symptoms).distinct() if symptoms else diseases
        # diseases = diseases.filter(geographical_area__in=all_areas) if all_world else diseases
        diseases = diseases.filter(geographical_area__in=geographical_area).distinct() if geographical_area else diseases

        ctx = {'diseases': diseases}
        return render(request, 'diseases_list.html', ctx)


class GeographicalAreaListView(SuccessMessageMixin, CreateView, ListView):
    """ Page with all geographical areas from DB. """

    model = GeographicalArea
    object_list = GeographicalArea.objects.all()
    form_class = GeographicalAreaCreateForm
    context_object_name = 'areas'
    template_name = 'geographical_areas_list.html'
    success_message = 'New area %(area)s successfully created!'
    success_url = reverse_lazy('geographical_areas_list')


class HomePageView(TemplateView):
    """ Start (home) page. """

    template_name = 'home_page.html'


class OrgansListView(ListView):
    """ Page with organs list from DB. """

    model = Organ
    context_object_name = 'organs'
    template_name = 'organs_list.html'


class OrganCreateView(SuccessMessageMixin, UserPassesTestMixin, CreateView):
    """ Adding new organ to DB. """
    model = Organ
    form_class = OrganCreateForm
    template_name = 'add_new_organ.html'
    success_message = 'New organ %(name)s successfully created!'
    success_url = reverse_lazy('organs_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Doctors').exists() or self.request.user.is_superuser


class RegistrationView(FormView):
    """ Registration page. """

    model = User
    form_class = UserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('log_in')

    def form_valid(self, form):
        """If the form is valid, register the user, send email and redirect to success URL."""

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

        subject = 'Welcome to MedicalWebSite'
        message = f'''
            {user.full_name}, welcome to MedicalWebSite! 
            Hope you are enjoying using our MedicalWebSite.
            Let's start http://medical-reference-book.herokuapp.com/
        '''
        recepient = str(form['email'].value())
        send_mail(
            subject, 
            message, 
            EMAIL_HOST_USER, 
            [recepient], 
            fail_silently = False
        )

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

    def form_valid(self, form):
        """Save the new user's password."""
        form.save()
        return super().form_valid(form)
