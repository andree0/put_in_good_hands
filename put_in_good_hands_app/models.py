from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch.dispatcher import receiver

from put_in_good_hands_app.validators import (
    validate_address,
    validate_pick_up_date,
    validate_zip_code,
)


@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    if sender.objects.filter(is_superuser=True).count() == 1:
        raise PermissionDenied

@receiver(pre_save, sender=User)
def save_user(sender, instance, **kwargs):
    if sender.objects.filter(is_superuser=True).count() == 1:
        raise PermissionDenied


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
    type = models.IntegerField(choices=TYPES, default=TYPES[0][0])
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT)
    address = models.CharField(max_length=128, validators=[validate_address])
    phone_number = models.PositiveIntegerField(validators=[
        MinValueValidator(100000000), MaxValueValidator(999999999)])
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=6, validators=[validate_zip_code],
                                help_text="XX-XXX")
    pick_up_date = models.DateField(validators=[validate_pick_up_date])
    pick_up_time = models.TimeField()
    pick_up_comment = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True, default=None)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} worków dla {self.institution} - " \
               f"{self.pick_up_date} {self.pick_up_time}"
