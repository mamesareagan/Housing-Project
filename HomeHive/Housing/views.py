from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from Housing.forms import BuildingForm
from django.db import transaction

from Housing.models import Amenity, Building


class BuildingClassView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'buildings': buildings})
    
class BuildingDetailView(View):
    template_name = 'building_details.html'

    def get(self, request, building_id):
        building = get_object_or_404(Building, pk=building_id)
        return render(request, self.template_name, {'building': building})

class UpdateBuildingView(View):
    template_name = 'update_building.html'

    def get(self, request, pk):
        building = Building.objects.prefetch_related('amenities').get(pk=pk)
        form = BuildingForm(instance=building)
        return render(request, self.template_name, {'form': form, 'building': building})

    def post(self, request, pk):
        building = Building.objects.get(pk=pk)
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            updated_building = form.save(commit=False)
            # Get the list of selected amenity names from the form data
            selected_amenity_names = request.POST.getlist('amenities')
            
            # Clear existing amenities of the building
            updated_building.amenities.clear()
            
            # Create or get Amenity objects based on selected names
            for amenity_name in selected_amenity_names:
                amenity, created = Amenity.objects.get_or_create(name=amenity_name)
                updated_building.amenities.add(amenity)
                
            # Save the updated building
            updated_building.save()
            
            # Redirect to the building details page of the updated building
            return redirect(reverse('building-details', kwargs={'building_id': updated_building.pk}))
        return render(request, self.template_name, {'form': form, 'building': building})


# class BuildingFormView(FormView):
#     template_name = 'building_form.html'
#     form_class = BuildingForm
#     success_url = reverse_lazy('building-view')  # Use the correct URL pattern name

#     def form_valid(self, form):
#         # Process the form data and create a model instance
#         building = form.save(commit=False)
#         # Here, you can do any additional processing of the form data before saving
#         # For example, you can set values for fields not included in the form
#         building.save()
#         return super().form_valid(form)
class BuildingFormView(View):
    def get(self, request):
        form = BuildingForm()
        return render(request, 'building_form.html', {'form': form})

    def post(self, request):
        form = BuildingForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                building = form.save(commit=False)  # Save the building instance

                # Get the selected amenity names from the form
                selected_amenities_names = form.cleaned_data['amenities']

                # Create new amenities in the database if they don't exist
                for amenity_name in selected_amenities_names:
                    Amenity.objects.get_or_create(name=amenity_name)

                # Query the Amenity model for instances based on selected names
                selected_amenities = Amenity.objects.filter(name__in=selected_amenities_names)

                # Save the building instance to get its ID
                building.save()

                # Add selected amenities to the building
                building.amenities.add(*selected_amenities)

                return redirect('building-view')
        else:
            return render(request, 'building_form.html', {'form': form})