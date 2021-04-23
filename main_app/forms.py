from django import forms

from .models import (
    Disease, DiseaseSymptom, GeographicalArea, 
    Organ, Symptom, Treatment, User
)


class DiseaseCreateForm(forms.ModelForm):
    """Create new disease form"""

    class Meta:
        """Meta class"""
        model = Disease
        fields = ['name', 'description', 'affected_organs', 'geographical_area', 'treatment']
        labels = {
            'name': 'Disease',
            'description': 'Description',
            'affected_organs': 'Affected organs',
            'geographical_area': 'Geographical Area',
            'treatment': 'Treatment'
        }
        widgets = {
            'name': forms.Textarea(attrs={'cols': 140, 'rows': 2}),
            'description': forms.Textarea(attrs={'cols': 140, 'rows': 5}),
            'geographical_area': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
            'affected_organs': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
            'treatment': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'})
        }


class DiseaseCreateForm2(forms.ModelForm):
    """Create new disease form 2"""

    class Meta:
        """Meta class"""
        model = DiseaseSymptom
        fields = ['symptom', 'symptom_frequency']
        labels = {
            'symptom': 'Symptom',
            'symptom_frequency': 'Symptom frequency'
        }
        widgets = {
            'symptom': forms.Select(),
            'symptom_frequency': forms.Select()
        }


DiseaseFormSet = forms.formset_factory(DiseaseCreateForm2, extra=10)


class DiseaseSearchForm(forms.ModelForm):
    """Form to search the disease."""

    def __init__(self, *args, **kwargs):
        super(DiseaseSearchForm, self).__init__(*args, **kwargs)
        self.fields['symptoms'].required = False
        self.fields['affected_organs'].required = False
        self.fields['geographical_area'].required = False

    class Meta:
        """Meta class"""
        model = Disease
        fields = ['symptoms', 'affected_organs', 'geographical_area']
        labels = {
            'symptoms': 'Symptoms',
            'affected_organs': 'Affected organs',
            'geographical_area': 'Geographical Area'
        }
        widgets = {
            'geographical_area': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
            'affected_organs': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
            'symptoms': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
        }


class ContactForm(forms.Form):
    """Form to send a message to admin."""

    sender = forms.CharField(
        label="Your Full Name", 
        max_length=255, 
        widget=forms.TextInput(attrs={'size': 50}),
        required=False
    )
    sender_email = forms.EmailField(
        label="Email Address", 
        widget=forms.EmailInput(attrs={'size': 50}),
        required=False
    )
    message_text = forms.CharField(
        label="Message Text", 
        widget=forms.Textarea(attrs={'cols': 70, 'rows': 4})
    )
    

class GeographicalAreaCreateForm(forms.ModelForm):
    """Create new treatment form"""
    class Meta:
        """Meta class"""
        model = GeographicalArea
        fields = ['area', 'image']
        widgets = {
            'area': forms.Textarea(attrs={'cols': 140, 'rows': 2, 'placeholder': 'New Geographical Area'})
        }


class OrganCreateForm(forms.ModelForm):
    """Create new organ form"""

    class Meta:
        """Meta class"""
        model = Organ
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 140, 'rows': 1, 'max_length': 255}),
            'description': forms.Textarea(attrs={'cols': 140, 'rows': 2})
        }


class SymptomCreateForm(forms.ModelForm):
    """Create new symptom form"""

    class Meta:
        """Meta class"""
        model = Symptom
        fields = ['name', 'affected_organ']
        widgets = {
            'name': forms.Textarea(attrs={'cols': 30, 'rows': 3, 'max_length': 255})
        }


class TreatmentsCreateForm(forms.ModelForm):
    """Create new treatment form"""
    class Meta:
        """Meta class"""
        model = Treatment
        fields = ['treatment']
        widgets = {
            'treatment': forms.Textarea(attrs={'cols': 140, 'rows': 2, 'placeholder': 'New Treatment'})
        }


class UserCreateForm(forms.ModelForm):
    """Create new user form."""
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """Meta class."""
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email',
            'medical_license', 'password', 'repeat_password'
        ]
        widgets = {
            'password': forms.PasswordInput,
            'repeat_password': forms.PasswordInput
        }

    def clean(self):
        """Method to validate the password."""
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeat_password']:
            self.add_error('password', 'Passwords do not match!')
        if User.objects.filter(username=cleaned_data['username']):
            self.add_error('username', 'This username is already taken, try another one!')


class UserUpdateForm(forms.ModelForm):
    """Update user's data form."""

    class Meta:
        """Meta class."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'medical_license']
