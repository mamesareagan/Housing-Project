from django.db import models
from django.core.validators import RegexValidator

from Housing.validators import validate_available_houses

# Create your models here.
class Building(models.Model):
    building_name = models.CharField(max_length=255, null=False, blank=False, default= 'HomeHive')
    owner = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    total_number_of_houses = models.PositiveIntegerField()
    available_houses = models.PositiveIntegerField()
    amenities = models.ManyToManyField('Amenity', blank=True)

    def __str__(self):
        return f"Building at {self.location},owner {self.owner} with {self.available_houses} houses available"
    
    def clean(self):
        validate_available_houses(self.total_number_of_houses, self.available_houses)

    def save(self, *args, **kwargs):
        self.clean()
        super(Building, self).save(*args, **kwargs)


class Amenity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

  
class Tenant(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'\d{10}', message='Invalid phone number format (XXX-XXX-XXXX)')],
    )
    building = models.ForeignKey('Building', on_delete=models.CASCADE, related_name='tenants', null=True, blank=True)
    number_of_rooms = models.PositiveIntegerField(default=1, null=False, blank=False)
    number_of_people = models.PositiveIntegerField(default=1,null=False, blank=False)

    def __str__(self):
        return self.name

# class Caretaker(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
