from django import forms

from Housing.choices import AmenityChoices
from Housing.models import Building

# class BuildingForm(forms.ModelForm):
#     class Meta:
#         model = Building
#         fields = ['owner', 'location', 'total_number_of_houses', 'available_houses']

class BuildingForm(forms.ModelForm):
    amenities = forms.MultipleChoiceField(choices=AmenityChoices.CHOICES, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Building
        fields = ['building_name', 'owner', 'location', 'total_number_of_houses', 'available_houses', 'amenities']
