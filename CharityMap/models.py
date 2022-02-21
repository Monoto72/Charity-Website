from django.db import models

# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    class Type(models.TextChoices):
        Store = '1',
        Bin = '2'

    type = models.CharField(
        max_length=2,
        choices=Type.choices,
        default=Type.Store
    )