from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class ValidateOnlyNumbers(BaseValidator):
    def __init__(self, n_digits):
        self.n_digits = n_digits

    def __call__(self, value):
        if not value.isdigit():
            raise ValidationError("Este campo deve conter apenas números.")
        if len(value) != self.n_digits:
            raise ValidationError(f"Este campo deve conter {self.n_digits} números.")
