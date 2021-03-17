from django import forms

from .models import Treatment


class TreatmentsCreateForm(forms.ModelForm):
    """Create new treatment form"""
    class Meta:
        """Meta class"""
        model = Treatment
        fields = ['treatment']
        widgets = {
            'treatment': forms.Textarea(attrs={'cols': 100, 'rows': 2})
        }

