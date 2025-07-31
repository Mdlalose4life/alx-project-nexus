from django.conf import settings
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    """
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data,
            'status_code': response.status_code
        }
        
        # Log the error
        logger.error(f"API Error: {exc} - Context: {context}")
        
        # Customize based on error type
        if response.status_code == 404:
            custom_response_data['message'] = 'Resource not found'
        elif response.status_code == 400:
            custom_response_data['message'] = 'Bad request'
        elif response.status_code == 401:
            custom_response_data['message'] = 'Authentication required'
        elif response.status_code == 403:
            custom_response_data['message'] = 'Permission denied'
        elif response.status_code >= 500:
            custom_response_data['message'] = 'Internal server error'
            # Don't expose internal details in production
            if not settings.DEBUG:
                custom_response_data['details'] = 'Please try again later'
        
        response.data = custom_response_data
    
    return response