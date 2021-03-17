from django import forms

from .models import GeographicalArea, Organ, Symptom, Treatment


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
            'name': forms.Textarea(attrs={'cols': 30, 'rows': 2, 'max_length': 255})
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

