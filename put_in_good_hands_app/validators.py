from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_zip_code(value):
    if len(value) != 6 or value[2] != '-':
        raise ValidationError(_("Zły format kodu pocztowego."))
    value_num = value.split('-')
    try:
        for i in value_num:
            int(i)
    except ValueError:
        raise ValidationError(_("Zły format kodu pocztowego."))


def validate_address(value):
    if value.isalpha():
        raise ValidationError(_("Podaj numer budynku."))


def validate_password(value):
    if value.isdigit():
        raise ValidationError(
            _("Password cannot contain only numbers !"))
    if value.islower():
        raise ValidationError(
            _("Password must contain one uppercase letter !"))
    if value.isupper():
        raise ValidationError(
            _("Password must contain one lowercase letter !"))
    if value.find(' ') != -1:
        raise ValidationError(
            _("Password cannot contain  whitespace !"))
    if value.isalpha():
        raise ValidationError(
            _("Password must contain one digit and one special character !"))
    if len(value) < 9:
        raise ValidationError(
            _("Password must be longer than 8 characters !"))
