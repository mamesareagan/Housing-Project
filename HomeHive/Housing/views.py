from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from Housing.forms import BuildingForm

from Housing.models import Building


class BuildingClassView(View):
    template_name = 'building_details.html'

    def get(self, request, *args, **kwargs):
        buildings = Building.objects.all()
        return render(request, self.template_name, {'buildings': buildings})
    


class BuildingFormView(FormView):
    template_name = 'building_form.html'
    form_class = BuildingForm
    success_url = reverse_lazy('building-view')  # Use the correct URL pattern name

    def form_valid(self, form):
        # Process the form data and create a model instance
        building = form.save(commit=False)
        # Here, you can do any additional processing of the form data before saving
        # For example, you can set values for fields not included in the form
        building.save()
        return super().form_valid(form)