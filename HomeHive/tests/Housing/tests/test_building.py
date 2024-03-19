from django.urls import reverse
from django.test import Client
import pytest

from Housing.models import Building

@pytest.mark.django_db
class TestBuildingView:
    def test_building_view(self, client):
        sample_building = Building.objects.create(owner='John Doe', location='Sample Location', total_number_of_houses=10, available_houses=5)
        queried_building = Building.objects.filter(owner='John Doe').first()

        # Perform assertions
        assert queried_building is not None  # Check if the queried building exists
        assert queried_building.owner == 'John Doe'  # Check if the owner matches
        assert queried_building.location == 'Sample Location'  # Check if the location matches
        assert queried_building.total_number_of_houses == 10  # Check if the total number of houses matches
        assert queried_building.available_houses == 5  # Check if the available houses matches
        response = client.get(reverse('building-view'))
        assert response.status_code == 200
        

# @pytest.mark.django_db
# class TestBuildingFormView:
#     def test_building_form_view(self, client, sample_building):
#         response = client.get(reverse('building-reg_view'))
#         assert response.status_code == 200
#         assert 'Building Form' in response.content.decode('utf-8')
