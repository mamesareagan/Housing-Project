"""
Signal handlers for updating models when certain actions occur.
"""

from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from Housing.models import Tenant, Building, TotalTenants

@receiver(post_save, sender=Tenant)
def update_available_houses_on_tenant_creation_or_update(sender, instance, created, **kwargs):
    """
    Signal receiver function to update available_houses on Tenant creation or update.
    """
    if not created:  # Ignore if it's an update
        return
    
    instance.building.available_houses -= 1
    instance.building.save()

@receiver(post_delete, sender=Tenant)
def update_available_houses_on_tenant_deletion(sender, instance, **kwargs):
    """
    Signal receiver function to update available_houses on Tenant deletion.
    """
    instance.building.available_houses += 1
    instance.building.save()

@receiver(post_save, sender=Building)
def create_total_tenants(sender, instance, created, **kwargs):
    """
    Signal receiver function to create TotalTenants instance when a Building is saved.
    """
    if created:
        TotalTenants.objects.create(building=instance, total_count=0)

@receiver(pre_delete, sender=Building)
def delete_total_tenants(sender, instance, **kwargs):
    """
    Signal receiver function to delete TotalTenants instance when a Building is deleted.
    """
    try:
        total_tenants = TotalTenants.objects.get(building=instance)
        total_tenants.total_count = 0  # Set total_count to zero
        total_tenants.save()  # Save the changes
        total_tenants.delete()  # Delete the TotalTenants instance
    except TotalTenants.DoesNotExist:
        pass

@receiver(post_save, sender=Tenant)
def update_total_tenants(sender, instance, created, **kwargs):
    """
    Signal receiver function to update TotalTenants when a new Tenant is created.
    """
    if created:
        building = instance.building
        total_tenants, _ = TotalTenants.objects.get_or_create(building=building)
        total_tenants.total_count += instance.number_of_people
        total_tenants.save()
 
@receiver(pre_delete, sender=Tenant)
def update_total_tenants_on_tenant_delete(sender, instance, **kwargs):
    """
    Signal receiver function to update TotalTenants when a Tenant is deleted.
    """
    building = instance.building
    total_tenants, _ = TotalTenants.objects.get_or_create(building=building)
    
    # Subtract the number of people associated with the deleted tenant from total count
    total_tenants.total_count -= instance.number_of_people
    total_tenants.save()
