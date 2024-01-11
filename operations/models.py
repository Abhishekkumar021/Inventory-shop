from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal


class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    area = models.DecimalField(max_digits=8, decimal_places=3, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=3, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, length, breadth, height, created_by):
        area = Decimal(length) * Decimal(breadth)
        volume = Decimal(length) * Decimal(height) * Decimal(breadth)
        area = round(area, 3)
        volume = round(volume, 3)

        box = cls(
            length=length,
            breadth=breadth,
            height=height,
            area=area,
            volume=volume,
            created_by=created_by,
        )
        box.save()
        return box
