from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import DetailView
from django.urls import reverse, reverse_lazy
from Housing.forms import BuildingForm, CaretakerForm, TenantForm
from django.db import transaction

from Housing.models import Amenity, Building, Caretaker, Tenant, TotalTenants

def get_tenant_id(request):
    """
    Retrieve the tenant ID based on the house number provided in the request.
    
    :param request: The HTTP request object.
    :return: JsonResponse containing the tenant ID if found, or an error message if not found.
    """
    house_number = request.GET.get('house_number')
    try:
        tenant = Tenant.objects.get(house_number=house_number)
        return JsonResponse({'tenant_id': tenant.id})
    except Tenant.DoesNotExist:
        return JsonResponse({'error': 'Tenant not found'}, status=404)

class BuildingClassView(View):
    """
    View class for displaying a list of buildings.
    """
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        """
        Retrieve all buildings and render the main template with the list of buildings.
        
        :param request: The HTTP request object.
        :return: Rendered HTML template with the list of buildings.
        """
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'buildings': buildings})
    
class BuildingDetailView(View):
    """
    View class for displaying details of a building.
    """
    template_name = 'building_details.html'

    def get(self, request, building_id):
        """
        Retrieve details of the specified building and render the building details template.
        
        :param request: The HTTP request object.
        :param building_id: The ID of the building to retrieve details for.
        :return: Rendered HTML template with the building details.
        """
        building = get_object_or_404(Building, pk=building_id)
        
        # Fetch TotalTenants instance associated with the building
        total_tenants = TotalTenants.objects.get(building=building)
        buildings = Building.objects.prefetch_related('amenities').all()
        # Pass building and total_tenants to the template
        return render(request, self.template_name, {'building': building, 'total_tenants': total_tenants, 'buildings': buildings})

class UpdateBuildingView(View):
    """
    View class for updating a building.
    """
    template_name = 'update_building.html'

    def get(self, request, pk):
        """
        Render the form for updating a building.
        
        :param request: The HTTP request object.
        :param pk: The ID of the building to update.
        :return: Rendered HTML template with the building update form.
        """
        building = Building.objects.prefetch_related('amenities').get(pk=pk)
        available_amenities = building.amenities.all()  # Access prefetched amenities

        # Pass the initial data containing the IDs of available amenities
        initial_data = {'amenities': available_amenities.values_list('id', flat=True)}

        form = BuildingForm(instance=building, initial=initial_data)
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'form': form, 'building': building, 'buildings': buildings})

    def post(self, request, pk):
        """
        Handle the form submission to update a building.
        
        :param request: The HTTP request object.
        :param pk: The ID of the building to update.
        :return: Redirect to the building details page after updating the building.
        """
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
    """
    View class for rendering the building form.
    """
    def get(self, request):
        """
        Render the form for creating a new building.
        
        :param request: The HTTP request object.
        :return: Rendered HTML template with the building form.
        """
        form = BuildingForm()
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, 'building_form.html', {'form': form, 'buildings': buildings})

    def post(self, request):
        """
        Handle the form submission to create a new building.
        
        :param request: The HTTP request object.
        :return: Redirect to the list of buildings view after creating the building.
        """
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
    """
    View class for deleting a building.
    """
    def post(self, request, pk):
        """
        Handle the deletion of a building.
        
        :param request: The HTTP request object.
        :param pk: The ID of the building to delete.
        :return: Redirect to the list of buildings view after deletion.
        """
        building = get_object_or_404(Building, pk=pk)

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            # Delete the associated amenities
            building.amenities.clear()
            # Delete the building
            building.delete()

        return redirect('building-view')

class TenantDetailView(View):
    """
    View class for displaying details of a tenant.
    """
    template_name = 'tenant_detail.html'

    def get(self, request, tenant_id):
        """
        Retrieve details of the specified tenant and render the tenant details template.
        
        :param request: The HTTP request object.
        :param tenant_id: The ID of the tenant to retrieve details for.
        :return: Rendered HTML template with the tenant details.
        """
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'tenant': tenant, 'buildings': buildings})

class UpdateTenantView(View):
    """
    View class for updating a tenant.
    """
    template_name = 'update_tenant.html'
    
    def get(self, request, tenant_id):
        """
        Render the form for updating a tenant.
        
        :param request: The HTTP request object.
        :param tenant_id: The ID of the tenant to update.
        :return: Rendered HTML template with the tenant update form.
        """
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        form = TenantForm(instance=tenant)
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'form': form, 'tenant_id': tenant_id, 'buildings': buildings})

    def post(self, request, tenant_id):
        """
        Handle the form submission to update a tenant.
        
        :param request: The HTTP request object.
        :param tenant_id: The ID of the tenant to update.
        :return: Redirect to the tenant details page after updating the tenant.
        """
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        form = TenantForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant-detail', tenant_id=tenant_id)
        return render(request, self.template_name, {'form': form, 'tenant_id': tenant_id})

class TenantDeleteView(View):
    """
    View class for deleting a tenant.
    """
    def get(self, request, tenant_id):
        """
        Handle the deletion of a tenant.
        
        :param request: The HTTP request object.
        :param tenant_id: The ID of the tenant to delete.
        :return: Redirect to the building details page after deletion.
        """
        tenant = get_object_or_404(Tenant, pk=tenant_id)
        building_id = tenant.building.id
        tenant.delete()
        return redirect('building-details', building_id=building_id)

class AddTenantToBuildingView(View):
    """
    View class for adding a tenant to a building.
    """
    template_name = 'add_tenant.html'

    def get(self, request, building_id):
        """
        Render the form for adding a tenant to the specified building.
        
        :param request: The HTTP request object.
        :param building_id: The ID of the building to which the tenant will be added.
        :return: Rendered HTML template with the add tenant form.
        """
        building = get_object_or_404(Building, pk=building_id)
        form = TenantForm()
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'form': form, 'building': building, 'buildings': buildings})

    def post(self, request, building_id):
        """
        Handle the form submission to add a tenant to the building.
        
        :param request: The HTTP request object.
        :param building_id: The ID of the building.
        :return: Redirect to the building details page after adding the tenant.
        """
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
    """
    View class for adding a caretaker to a building.
    """
    template_name = 'add_Caretaker.html'

    def get(self, request, building_id):
        """
        Render the form for adding a caretaker to the specified building.
        
        :param request: The HTTP request object.
        :param building_id: The ID of the building to which the caretaker will be added.
        :return: Rendered HTML template with the add caretaker form.
        """
        building = get_object_or_404(Building, pk=building_id)
        form = CaretakerForm()
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'form': form, 'building': building, 'buildings': buildings})

    def post(self, request, building_id):
        """
        Handle the form submission to add a caretaker to the building.
        
        :param request: The HTTP request object.
        :param building_id: The ID of the building.
        :return: Redirect to the building details page after adding the caretaker.
        """
        building = get_object_or_404(Building, pk=building_id)
        form = CaretakerForm(request.POST)
        if form.is_valid():
            Caretaker = form.save(commit=False)
            Caretaker.building = building
            Caretaker.save()
            return redirect('building-details', building_id=building_id)
        return render(request, self.template_name, {'form': form, 'building': building})

class UpdateCaretakerView(View):
    """
    View class for updating a caretaker.
    """
    template_name = 'update_caretaker.html'

    def get(self, request, pk):
        """
        Render the form for updating a caretaker.
        
        :param request: The HTTP request object.
        :param pk: The ID of the caretaker to update.
        :return: Rendered HTML template with the caretaker update form.
        """
        caretaker = get_object_or_404(Caretaker, pk=pk)
        building = caretaker.building
        form = CaretakerForm(instance=caretaker)
        buildings = Building.objects.prefetch_related('amenities').all()
        return render(request, self.template_name, {'form': form, 'building': building, 'caretaker': caretaker, 'buildings': buildings})

    def post(self, request, pk):
        """
        Handle the form submission to update a caretaker.
        
        :param request: The HTTP request object.
        :param pk: The ID of the caretaker to update.
        :return: Redirect to the building details page after updating the caretaker.
        """
        caretaker = get_object_or_404(Caretaker, pk=pk)
        building = caretaker.building

        form = CaretakerForm(request.POST, instance=caretaker)
        if form.is_valid():
            form.save()
            return redirect(reverse('building-details', kwargs={'building_id': building.pk}))

        return render(request, self.template_name, {'form': form, 'building': building, 'caretaker': caretaker})

class DeleteCaretakerView(View):
    """
    View class for deleting a caretaker.
    """
    def post(self, request, pk):
        """
        Handle the deletion of a caretaker.
        
        :param request: The HTTP request object.
        :param pk: The ID of the caretaker to delete.
        :return: Redirect to the building details page after deletion.
        """
        caretaker = get_object_or_404(Caretaker, pk=pk)
        building = caretaker.building

        caretaker.delete()
        return redirect('building-details', building_id=building.pk)
