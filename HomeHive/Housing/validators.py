from django.core.exceptions import ValidationError

@staticmethod
def validate_available_houses(no_of_houses, available_houses_value):
    if available_houses_value > no_of_houses:
        raise ValidationError("The value of available house can't be greater than the number of houses")

