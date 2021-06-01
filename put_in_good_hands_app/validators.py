import datetime

from django.core.exceptions import ValidationError


def validate_zip_code(value):
    if len(value) != 6 or value[2] != '-':
        raise ValidationError("Zły format kodu pocztowego.")
    value_num = value.split('-')
    try:
        for i in value_num:
            int(i)
    except ValueError:
        raise ValidationError("Zły format kodu pocztowego.")


def validate_address(value):
    if value.isalpha():
        raise ValidationError("Podaj numer budynku.")


def validate_pick_up_date(value):
    if value <= datetime.date.today():
        raise ValidationError("Podany termin jest niedostęþny.")
