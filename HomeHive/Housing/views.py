from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse, reverse_lazy
from Housing.forms import BuildingForm, CaretakerForm, TenantForm
from django.db import transaction

from Housing.models import Amenity, Building, Caretaker, Tenant


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
        
class DeleteBuildingView(View):
    def post(self, request, pk):
        building = get_object_or_404(Building, pk=pk)

        building.delete()
        
        return redirect('building-view')  
        
class AddTenantToBuildingView(View):
    template_name = 'add_tenant.html'

    def get(self, request, building_id):
        building = get_object_or_404(Building, pk=building_id)
        form = TenantForm()
        return render(request, self.template_name, {'form': form, 'building': building})

    def post(self, request, building_id):
        building = get_object_or_404(Building, pk=building_id)
        form = TenantForm(request.POST)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.building = building
            tenant.save()
            return redirect('building-details', building_id=building_id)
        return render(request, self.template_name, {'form': form, 'building': building})
    
   
class AddCaretakerToBuildingView(View):
    template_name = 'add_Caretaker.html'

    def get(self, request, building_id):
        building = get_object_or_404(Building, pk=building_id)
        form = CaretakerForm()
        return render(request, self.template_name, {'form': form, 'building': building})

    def post(self, request, building_id):
        building = get_object_or_404(Building, pk=building_id)
        form = CaretakerForm(request.POST)
        if form.is_valid():
            Caretaker = form.save(commit=False)
            Caretaker.building = building
            Caretaker.save()
            return redirect('building-details', building_id=building_id)
        return render(request, self.template_name, {'form': form, 'building': building})
    
class UpdateCaretakerView(View):
    template_name = 'update_caretaker.html'

    def get(self, request, pk):
        building = Building.objects.prefetch_related('caretaker').get(pk=pk)
        form = CaretakerForm(instance=building)
        return render(request, self.template_name, {'form': form, 'building': building})

    def post(self, request, pk):
        # Retrieve the caretaker instance to update
        caretaker = Caretaker.objects.get(pk=pk)
        
        if request.method == 'POST':
            # Bind the form data to this caretaker instance
            form = CaretakerForm(request.POST, instance=caretaker)
            if form.is_valid():
                # Save the updated caretaker
                form.save()
                
                # Get the building associated with the caretaker
                building = caretaker.building
                
                # Redirect to the building details page
                return redirect(reverse('building-details', kwargs={'building_id': building.pk}))
        else:
            # Create the form instance with the caretaker data filled in
            form = CaretakerForm(instance=caretaker)
        
        # If form is not valid or it's a GET request, render the form again with the errors
        return render(request, self.template_name, {'form': form, 'building': caretaker.building})
