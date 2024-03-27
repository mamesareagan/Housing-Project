from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from Housing.models import Tenant, Building

@receiver(post_save, sender=Tenant)
def update_available_houses_on_tenant_creation_or_update(sender, instance, created, **kwargs):
    if not created:  # Ignore if it's an update
        return
    
    instance.building.available_houses -= 1
    instance.building.save()

@receiver(post_delete, sender=Tenant)
def update_available_houses_on_tenant_deletion(sender, instance, **kwargs):
    instance.building.available_houses += 1
    instance.building.save()
