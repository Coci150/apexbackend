import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import Contact
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .admin import ContactAdmin

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submissions"""
    try:
        data = json.loads(request.body)

        # Validate required fields
        if not data.get('name') or not data.get('email'):
            return JsonResponse({
                'status': 'error',
                'message': 'Name and email are required'
            }, status=400)

        # Save to database
        contact = Contact.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            company=data.get('company', ''),
            message=data.get('message', ''),
            ip_address=get_client_ip(request)
        )

        # Send email notification (if email settings are configured)
        try:
            subject = f"New Contact Form Submission from {data.get('name')}"
            message_body = f"""
Name: {data.get('name')}
Email: {data.get('email')}
Company: {data.get('company', 'Not provided')}

Message:
{data.get('message', 'No message provided')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
View in admin: http://{request.get_host()}/admin/core/contact/{contact.id}/change/
            """

            send_mail(
                subject=subject,
                message=message_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=True,  # Don't fail if email doesn't send
            )
            logger.info(f"Email sent for {data.get('email')}")
        except Exception as e:
            logger.error(f"Email failed: {str(e)}")
            # Continue - we still want to return success

        return JsonResponse({
            'status': 'success',
            'message': 'Thank you! We\'ll contact you soon.'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Server error occurred'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Handle newsletter subscriptions"""
    try:
        data = json.loads(request.body)
        email = data.get('email')

        if not email:
            return JsonResponse({
                'status': 'error',
                'message': 'Email is required'
            }, status=400)

        # Validate email format (basic validation)
        if '@' not in email or '.' not in email:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid email format'
            }, status=400)

        # Here you would typically save to database
        # For now, just return success

        return JsonResponse({
            'status': 'success',
            'message': 'Successfully subscribed to newsletter!'
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Newsletter error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Server error occurred'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint - verifies API is working"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'Apex Creatives API',
        'version': '1.0.0',
        'database': 'connected',
        'email_configured': hasattr(settings, 'CONTACT_RECIPIENT_EMAIL')
    })

@staff_member_required
def campaign_stats_view(request):
    """Wrapper view for campaign statistics"""
    # Create admin instance properly
    admin_instance = ContactAdmin(model=Contact, admin_site=admin.site)
    return admin_instance.campaign_stats_view(request)