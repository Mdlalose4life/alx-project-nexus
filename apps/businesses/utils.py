from django.utils.text import slugify
from django.utils.crypto import get_random_string
import re

def clean_business_name_for_slug(name):
    """
    Clean business name for better slug generation
    Handles common business name patterns in townships
    """
    # Remove common business suffixes/prefixes
    cleaning_patterns = [
        r'\b(pty|ltd|cc|inc|corp|company|co)\b',  # Legal entities
        r'\b(shop|store|market|spaza)\b',          # Common business words
        r'\b(the|and|&)\b',                       # Articles and conjunctions
        r'[^\w\s-]',                              # Special characters except hyphens
    ]
    
    cleaned = name.lower()
    for pattern in cleaning_patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra spaces and hyphens
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def generate_township_friendly_slug(business_name, city=None, business_type=None):
    """
    Generate SEO-friendly slugs for township businesses
    """
    # Clean the business name
    cleaned_name = clean_business_name_for_slug(business_name)
    base_slug = slugify(cleaned_name)
    
    # Add location context if provided
    if city:
        # Handle township names specifically
        city_clean = city.lower()
        if 'township' in city_clean:
            city_clean = city_clean.replace('township', '').strip()
        base_slug = f"{base_slug}-{slugify(city_clean)}"
    
    return base_slug