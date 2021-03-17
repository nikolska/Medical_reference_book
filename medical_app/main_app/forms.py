from django import forms

from .models import GeographicalArea, Treatment


class GeographicalAreaCreateForm(forms.ModelForm):
    """Create new treatment form"""
    class Meta:
        """Meta class"""
        model = GeographicalArea
        fields = ['area', 'image']
        widgets = {
            'area': forms.Textarea(attrs={'cols': 140, 'rows': 2})
        }


class TreatmentsCreateForm(forms.ModelForm):
    """Create new treatment form"""
    class Meta:
        """Meta class"""
        model = Treatment
        fields = ['treatment']
        widgets = {
            'treatment': forms.Textarea(attrs={'cols': 140, 'rows': 2})
        }

