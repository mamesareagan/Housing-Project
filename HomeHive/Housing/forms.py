"""
Forms for handling data input and validation in the Housing application.
"""

from django import forms
from Housing.choices import AmenityChoices
from Housing.models import Building, Caretaker, Tenant

class BuildingForm(forms.ModelForm):
    """
    Form for creating or updating a Building object.

    Attributes:
        amenities (MultipleChoiceField): Field for selecting amenities available in the building.
    """
    amenities = forms.MultipleChoiceField(choices=AmenityChoices.CHOICES, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        """
        Meta class specifying the model and fields for the form.
        """
        model = Building
        fields = ('building_name', 'owner', 'location', 'total_number_of_houses', 'amenities')

class TenantForm(forms.ModelForm):
    """
    Form for creating or updating a Tenant object.
    """
    class Meta:
        """
        Meta class specifying the model and fields for the form.
        """
        model = Tenant
        fields = ['name', 'phone_number', 'house_number', 'number_of_rooms', 'number_of_people']

class CaretakerForm(forms.ModelForm):
    """
    Form for creating or updating a Caretaker object.
    """
    class Meta:
        """
        Meta class specifying the model and fields for the form.
        """
        model = Caretaker
        fields = ['name', 'phone_number']
