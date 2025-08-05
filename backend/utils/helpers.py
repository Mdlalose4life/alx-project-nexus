from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from decimal import Decimal
import uuid
import os

def generate_unique_filename(instance, filename):
    """
    Generate unique filename for uploaded files
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return filename

def calculate_distance(point1, point2):
    """
    Calculate distance between two points in kilometers
    """
    if not point1 or not point2:
        return None
    
    try:
        return point1.distance(point2) * 111  # Convert degrees to km
    except:
        return None

def geocode_address(address):
    """
    Geocode an address to get coordinates
    This is a placeholder - implement with your preferred geocoding service
    """
    # Example with Google Geocoding API
    # import googlemaps
    # gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    # geocode_result = gmaps.geocode(address)
    # if geocode_result:
    #     location = geocode_result[0]['geometry']['location']
    #     return Point(location['lng'], location['lat'])
    return None

def format_currency(amount, currency='ZAR'):
    """
    Format currency for South African Rand
    """
    if currency == 'ZAR':
        return f"R{amount:,.2f}"
    return f"{amount:,.2f} {currency}"

def calculate_discount_percentage(original_price, current_price):
    """
    Calculate discount percentage
    """
    if not original_price or original_price <= current_price:
        return 0
    
    discount = ((original_price - current_price) / original_price) * 100
    return round(discount, 2)
