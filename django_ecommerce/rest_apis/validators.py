from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Customer

import re

def validate_email(value):
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(pat,value):
        raise serializers.ValidationError(f'{value} is not a valid email format!!')
    return value

unique_email = UniqueValidator(queryset=Customer.objects.all())