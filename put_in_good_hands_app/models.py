from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Institution(models.Model):
    TYPES = (
        (0, 'fundacja'),
        (1, 'organizacja pozarządowa'),
        (2, 'zbiórka lokalna'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.IntegerField(choices=TYPES, default=TYPES[0])
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL)
    address = models.CharField(max_length=255)
    phone_number = models.PositiveIntegerField()
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             default=models.SET_NULL)
