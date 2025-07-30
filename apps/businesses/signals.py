from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Business
from django.utils.text import slugify
from django.utils.crypto import get_random_string

@receiver(pre_save, sender=Business)
def set_business_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)

        if not Business.objects.filter(slug=base_slug).exists():
            instance.slug = base_slug
            return

        city_slug = f"{base_slug}-{slugify(instance.city)}"
        if not Business.objects.filter(slug=city_slug).exists():
            instance.slug = city_slug
            return

        type_slug = f"{base_slug}-{slugify(instance.get_business_type_display())}"
        if not Business.objects.filter(slug=type_slug).exists():
            instance.slug = type_slug
            return

        # Fallback to random suffix
        instance.slug = f"{base_slug}-{get_random_string(6).lower()}"
