from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
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
        available_amenities = building.amenities.all()  # Access prefetched amenities

        # Pass the initial data containing the IDs of available amenities
        initial_data = {'amenities': available_amenities.values_list('id', flat=True)}

        form = BuildingForm(instance=building, initial=initial_data)

        return render(request, self.template_name, {'form': form, 'building': building})



    def post(self, request, pk):
        building = get_object_or_404(Building, pk=pk)
        form = BuildingForm(request.POST, instance=building)

        # Fetch all available amenities associated with the building
        available_amenities = building.amenities.all()

        if form.is_valid():
            updated_building = form.save(commit=False)
            # Clear existing amenities of the building
            updated_building.amenities.clear()

            # Get the list of selected amenity names from the form data
            selected_amenity_names = request.POST.getlist('amenities')

            # Create or get Amenity objects based on selected names
            for amenity_name in selected_amenity_names:
                amenity, created = Amenity.objects.get_or_create(name=amenity_name)
                updated_building.amenities.add(amenity)

            # Save the updated building
            updated_building.save()

            # Redirect to the building details page of the updated building
            return redirect(reverse('building-details', kwargs={'building_id': updated_building.pk}))

        return render(request, self.template_name, {'form': form, 'building': building, 'available_amenities': available_amenities})


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
    
class TenantDetailView(View):
    template_name = 'tenant_detail.html'

    def get(self, request, tenant_id):
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'tenant': tenant, 'buildings': buildings})

class UpdateTenantView(View):
    template_name = 'update_tenant.html'
    buildings = Building.objects.prefetch_related('amenities').all()
    def get(self, request, tenant_id):
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        form = TenantForm(instance=tenant)
        return render(request, self.template_name, {'form': form, 'tenant_id': tenant_id})

    def post(self, request, tenant_id):
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant-detail', tenant_id=tenant_id)
        return render(request, self.template_name, {'form': form, 'tenant_id': tenant_id})


class TenantDeleteView(View):
    def get(self, request, tenant_id):
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        building_id = tenant.building.id
        tenant.delete()
        return redirect('building-details', building_id=building_id)


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
            house_number = form.cleaned_data['house_number']
            if Tenant.objects.filter(building=building, house_number=house_number).exists():
                form.add_error('house_number', f'House number {house_number} is occupied.')
                return render(request, self.template_name, {'form': form, 'building': building})
            else:
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
        caretaker = get_object_or_404(Caretaker, pk=pk)
        building = caretaker.building
        form = CaretakerForm(instance=caretaker)
        return render(request, self.template_name, {'form': form, 'building': building, 'caretaker': caretaker})

    def post(self, request, pk):
        caretaker = get_object_or_404(Caretaker, pk=pk)
        building = caretaker.building

        form = CaretakerForm(request.POST, instance=caretaker)
        if form.is_valid():
            form.save()
            return redirect(reverse('building-details', kwargs={'building_id': building.pk}))

        return render(request, self.template_name, {'form': form, 'building': building, 'caretaker': caretaker})

class DeleteCaretakerView(View):
    def post(self, request, pk):
        caretaker = get_object_or_404(Caretaker, pk=pk)
        building = caretaker.building

        caretaker.delete()
        return redirect('building-details', building_id=building.pk)