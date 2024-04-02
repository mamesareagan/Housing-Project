from email.policy import default
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

from Housing.validators import validate_available_houses
class Building(models.Model):
    """
    Represents a building with its attributes.

    Attributes:
        building_name (str): The name of the building.
        owner (str): The owner of the building.
        location (str): The location of the building.
        total_number_of_houses (int): The total number of houses in the building. Must be greater than or equal to 1.
        available_houses (int): The number of available houses in the building. Initially set to total_number_of_houses.
        amenities (ManyToManyField): The amenities available in the building.
    """
    building_name = models.CharField(max_length=255, null=False, blank=False, default='HomeHive')
    owner = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    total_number_of_houses = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_houses = models.PositiveIntegerField()
    amenities = models.ManyToManyField('Amenity', blank=True)

    def __str__(self):
        """
        Returns a string representation of the Building object.

        Returns:
            str: A string representation of the Building object.
        """
        return f"Building at {self.location}, owner {self.owner} with {self.available_houses} houses available"

    def save(self, *args, **kwargs):
        """
        Custom save method to set available_houses initially equal to total_number_of_houses when creating a new building.
        """
        if not self.pk:
            self.available_houses = self.total_number_of_houses

        validate_available_houses(self.total_number_of_houses, self.available_houses) 
        super(Building, self).save(*args, **kwargs)  

class Amenity(models.Model):
    """
    Represents an amenity available in a building.

    Attributes:
        name (str): The name of the amenity.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the Amenity object.

        Returns:
            str: A string representation of the Amenity object.
        """
        return f"Amenity: {self.name}"

class Tenant(models.Model):
    """
    Represents a tenant occupying a house in a building.

    Attributes:
        name (str): The name of the tenant.
        house_number (str): The house number occupied by the tenant.
        phone_number (str): The phone number of the tenant.
        building (ForeignKey): The building where the tenant resides.
        number_of_rooms (int): The number of rooms occupied by the tenant. Must be greater than or equal to 1.
        number_of_people (int): The number of people living in the tenant's house. Must be greater than or equal to 1.
    """
    name = models.CharField(max_length=20)
    house_number = models.CharField(max_length=10)
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'\d{10}', message='Invalid phone number format (XXX-XXX-XXXX)')],
    )
    building = models.ForeignKey('Building', on_delete=models.CASCADE, related_name='tenants', null=False, blank=False)
    number_of_rooms = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    number_of_people = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=False, blank=False)

    def __str__(self):
        """
        Returns a string representation of the Tenant object.

        Returns:
            str: A string representation of the Tenant object.
        """
        return self.name

class TotalTenants(models.Model):
    """
    Represents the total count of tenants in a building.

    Attributes:
        building (OneToOneField): The building for which the total tenant count is recorded.
        total_count (int): The total count of tenants.
    """
    building = models.OneToOneField(Building, on_delete=models.CASCADE)
    total_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the TotalTenants object.

        Returns:
            str: A string representation of the TotalTenants object.
        """
        return f"Total Tenants for {self.building.building_name} = {self.total_count}"

class Caretaker(models.Model):
    """
    Represents a caretaker responsible for managing a building.

    Attributes:
        name (str): The name of the caretaker.
        building (ForeignKey): The building associated with the caretaker.
        phone_number (str): The phone number of the caretaker.
    """
    name = models.CharField(max_length=255, null=False, blank=False)
    building = models.ForeignKey('Building', on_delete=models.CASCADE, related_name='caretaker', null=False, blank=False)
    phone_number = models.CharField(max_length=20,
        validators=[RegexValidator(regex=r'\d{10}', message='Invalid phone number format (XXX-XXX-XXXX)')],
    )
    def __str__(self):
        """
        Returns a string representation of the Caretaker object.

        Returns:
            str: A string representation of the Caretaker object.
        """
        return f"Caretaker: {self.name}"