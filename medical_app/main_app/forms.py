from django import forms

from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment


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

