from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import datetime

def health_check(request):
    """Basic health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0',
        'environment': getattr(settings, 'ENVIRONMENT', 'development'),
        'debug': settings.DEBUG
    })

def database_check(request):
    """Database connectivity check"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    # Test cache if available
    cache_status = 'not_configured'
    try:
        cache.set('health_check', 'test', 30)
        if cache.get('health_check') == 'test':
            cache_status = 'connected'
        else:
            cache_status = 'error'
    except Exception as e:
        cache_status = f'error: {str(e)}'
    
    return JsonResponse({
        'status': 'healthy' if db_status == 'connected' else 'unhealthy',
        'database': db_status,
        'cache': cache_status,
        'timestamp': datetime.datetime.now().isoformat()
    })