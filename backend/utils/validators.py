from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_south_african_phone(value):
    """
    Validate South African phone numbers
    Accepts formats: +27123456789, 0123456789, 123456789
    """
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]', '', value)
    
    # Check various SA phone number formats
    patterns = [
        r'^\+27[1-9]\d{8}',  # +27123456789
        r'^0[1-9]\d{8}',     # 0123456789
        r'^[1-9]\d{8}',      # 123456789
    ]
    
    if not any(re.match(pattern, cleaned) for pattern in patterns):
        raise ValidationError(
            _('Enter a valid South African phone number.'),
            code='invalid_phone'
        )

def validate_business_registration(value):
    """
    Validate South African business registration number
    Format: YYYY/NNNNNN/NN
    """
    pattern = r'^\d{4}/\d{6}/\d{2}'
    
    if not re.match(pattern, value):
        pattern = r'^\d{4}/\d{6}/\d{2}'
    
    if not re.match(pattern, value):
        raise ValidationError(
            _('Enter a valid business registration number (YYYY/NNNNNN/NN).'),
            code='invalid_registration'
        )
