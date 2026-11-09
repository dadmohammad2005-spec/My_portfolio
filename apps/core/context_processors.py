from .models import SiteSettings

def site_settings(request):
    """
    Context processor to make site settings globally available across all templates.
    """
    try:
        settings_obj = SiteSettings.load()
    except Exception:
        settings_obj = None

    unread_count = 0
    if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
        try:
            from apps.contact.models import ContactMessage
            unread_count = ContactMessage.objects.filter(is_read=False).count()
        except Exception:
            unread_count = 0

    return {
        'site_settings': settings_obj,
        'unread_count': unread_count,
    }
