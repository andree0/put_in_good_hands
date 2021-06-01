from django.core.exceptions import ValidationError


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
