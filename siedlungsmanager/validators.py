# shop/validators.py

from django.core.exceptions import ValidationError


def validate_last_decimal_for_currency(value):
    decimal_part = (value * 100) % 10
    if decimal_part not in (0, 5):
        raise ValidationError('The last decimal place must be 0 or 5')
