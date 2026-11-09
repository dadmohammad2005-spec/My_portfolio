from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import logging

from .forms import ContactForm
from .models import ContactMessage

logger = logging.getLogger(__name__)

class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, 'contact.html', {'form': form})

    def post(self, request, *args, **kwargs):
        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or
            'application/json' in request.headers.get('accept', '')
        )

        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract sender IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')

            contact_msg = form.save(commit=False)
            contact_msg.ip_address = ip
            contact_msg.save()

            # Email notification
            try:
                subject_line = f"New Portfolio Inquiry: {contact_msg.subject} from {contact_msg.name}"
                email_body = (
                    f"You have received a new contact submission from your portfolio website:\n\n"
                    f"Name: {contact_msg.name}\n"
                    f"Email: {contact_msg.email}\n"
                    f"Subject: {contact_msg.subject}\n"
                    f"IP: {ip}\n\n"
                    f"Message:\n{contact_msg.message}\n"
                )
                send_mail(
                    subject=subject_line,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Failed to dispatch contact notification email: {e}")

            success_message = "Thank you! Your message has been sent successfully. I will get back to you shortly."
            if is_ajax:
                return JsonResponse({'success': True, 'message': success_message})

            messages.success(request, success_message)
            return redirect('contact:index')

        else:
            # Form validation errors
            if is_ajax:
                errors = {field: [str(err) for err in error_list] for field, error_list in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)

            messages.error(request, "Please correct the highlighted errors below.")
            return render(request, 'contact.html', {'form': form})
