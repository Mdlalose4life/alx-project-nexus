# utils/notifications.py (Optional - for future notification system)
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class OrderNotificationService:
    """
    Service class for handling order-related notifications
    """
    
    @staticmethod
    def send_order_confirmation(order):
        """Send order confirmation email to customer"""
        subject = f'Order Confirmation - {order.order_number}'
        context = {
            'order': order,
            'customer': order.customer,
            'business': order.business,
        }
        
        # Render email template
        html_message = render_to_string('emails/order_confirmation.html', context)
        plain_message = render_to_string('emails/order_confirmation.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_status_update(order, old_status, new_status):
        """Send order status update to customer"""
        subject = f'Order Update - {order.order_number}'
        context = {
            'order': order,
            'old_status': old_status,
            'new_status': new_status,
            'customer': order.customer,
            'business': order.business,
        }
        
        html_message = render_to_string('emails/order_status_update.html', context)
        plain_message = render_to_string('emails/order_status_update.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_business_notification(order, message_type):
        """Send notification to business owner"""
        subject_map = {
            'new_order': f'New Order Received - {order.order_number}',
            'cancelled': f'Order Cancelled - {order.order_number}',
        }
        
        subject = subject_map.get(message_type, f'Order Update - {order.order_number}')
        context = {
            'order': order,
            'business': order.business,
            'message_type': message_type,
        }
        
        html_message = render_to_string('emails/business_notification.html', context)
        plain_message = render_to_string('emails/business_notification.txt', context)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.business.email] if order.business.email else [],
            html_message=html_message,
            fail_silently=False,
        )