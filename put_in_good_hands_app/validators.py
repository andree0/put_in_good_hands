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


def validate_password(value):
    special_mark = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    if value.isdigit():
        raise ValidationError("Hasło nie może składać się z samych cyfr.")
    if value.islower():
        raise ValidationError("Hasło musi zawierać dużą literę.")
    if value.isupper():
        raise ValidationError("Hasło musi zawierać małą literę.")
    if value.find(' ') != -1:
        raise ValidationError("Hasło nie może zawierać białych znaków.")
    if value.isalpha():
        raise ValidationError(
            "Hasło musi zawierać cyfrę i znak specjalny.")
    if len(value) < 8:
        raise ValidationError("Hasło musi zawierać minimum 8 znaków. ")
    if not [mark for mark in special_mark if mark in value]:
        raise ValidationError(f"Hasło musi zawierać znak specjalny {special_mark} ")
