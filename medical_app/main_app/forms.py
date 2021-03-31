from django import forms

from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment, User


class DiseaseCreateForm(forms.ModelForm):
    """Create new disease form"""

    symptom_frequency = forms.ChoiceField(choices=DiseaseSymptom.SYMPTOM_FREQUENCY_CHOICES)

    class Meta:
        """Meta class"""
        model = Disease
        fields = ['name', 'description', 'symptoms', 'affected_organs', 'geographical_area', 'treatment']
        labels = {
            'name': 'Disease',
            'description': 'Description',
            'symptoms': 'Symptoms',
            'affected_organs': 'Affected organs',
            'geographical_area': 'Geographical Area',
            'treatment': 'Treatment'
        }
        widgets = {
            'name': forms.Textarea(attrs={'cols': 140, 'rows': 2}),
            'description': forms.Textarea(attrs={'cols': 140, 'rows': 5}),
            'geographical_area': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
            'affected_organs': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'}),
            'symptoms': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'},
                                                     choices=DiseaseSymptom.SYMPTOM_FREQUENCY_CHOICES),
            'treatment': forms.CheckboxSelectMultiple({'class': 'no-bullet-list'})
        }


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

