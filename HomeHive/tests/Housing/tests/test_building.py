from django.forms import ValidationError
from django.urls import reverse
import pytest

from Housing.models import Building

@pytest.mark.django_db
class TestBuildingView:
    @pytest.fixture(autouse=True)
    def setup(self):  # No arguments needed here
        from django.test import Client  # Import Client inside the fixture

        self.client = Client()
    def test_building_view(self):
        sample_building = Building.objects.create(owner='John Doe', location='Sample Location', total_number_of_houses=10, available_houses=5)
        queried_building = Building.objects.filter(owner='John Doe').first()

        # Perform assertions
        assert queried_building is not None  # Check if the queried building exists
        assert queried_building.owner == 'John Doe'  # Check if the owner matches
        assert queried_building.location == 'Sample Location'  # Check if the location matches
        assert queried_building.total_number_of_houses == 10  # Check if the total number of houses matches
        assert queried_building.available_houses == 5  # Check if the available houses matches
        response = self.client.get(reverse('building-view'))
        assert response.status_code == 200

        with pytest.raises(ValidationError) as exc_info:  # Context manager to capture the expected exception
            sample_building = Building.objects.create(
                owner='John Doe',
                location='Sample Location',
                total_number_of_houses=10,
                available_houses=12  # Set available_houses higher than total_number_of_houses
            )
            assert "available_houses cannot be greater than total_number_of_houses" in str(exc_info.value)
    
    # def test_building_update(self):
    #     # Create a sample building
    #     sample_building = Building.objects.create(owner='John Doe', location='Sample Location', total_number_of_houses=10, available_houses=5)
    
    #     # URL for building update view
    #     url = reverse('building-update', kwargs={'pk': sample_building.pk})
        
    #     # Simulate GET request to fetch the form with initial building data
    #     response = self.client.get(url)
        
    #     # Assert status code for successful GET request
    #     assert response.status_code == 200
        
    #     # Prepare update data
    #     update_data = {
    #         'owner': 'Jane Doe',
    #         'location': 'New Location',
    #         'total_number_of_houses': 15,
    #         'available_houses': 8,
    #     }
        
    #     # Simulate POST request to update the building
    #     response = self.client.post(url, update_data)
        
    #     # Assert successful update (HTTP status code 302 for redirect)
    #     assert response.status_code == 200
        
    #     # Fetch the updated building from the database
    #     updated_building = Building.objects.get(pk=sample_building.pk)
        
    #     # Assert updated values
    #     assert updated_building.owner == update_data['owner']
    #     assert updated_building.location == update_data['location']
    #     assert updated_building.total_number_of_houses == update_data['total_number_of_houses']
    #     assert updated_building.available_houses == update_data['available_houses']

        

@pytest.mark.django_db
class TestBuildingFormView:
    @pytest.fixture(autouse=True)
    def setup(self):  # No arguments needed here
        from django.test import Client  # Import Client inside the fixture

        self.client = Client()

    def test_building_form_view(self):
        response = self.client.get(reverse('building-reg_view'))
        assert response.status_code == 200  # Check if the form view is accessible
        assert 'Building Form' in response.content.decode('utf-8')
       