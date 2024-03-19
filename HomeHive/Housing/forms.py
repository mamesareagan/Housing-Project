from django import forms
from .models import Building

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['owner', 'location', 'total_number_of_houses', 'available_houses']
