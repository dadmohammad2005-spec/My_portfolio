from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status_badge', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip_address', 'created_at')
    actions = ['mark_as_read', 'mark_as_unread']
    ordering = ('-created_at',)

    fieldsets = (
        ("Sender Details", {
            "fields": ("name", "email", "ip_address", "created_at")
        }),
        ("Message Content", {
            "fields": ("subject", "message")
        }),
        ("Status", {
            "fields": ("is_read",)
        }),
    )

    def status_badge(self, obj):
        if obj.is_read:
            return format_html('<span style="color: #64748b; font-weight: 500;">✓ Read</span>')
        return format_html('<span style="color: #0d9488; font-weight: 700; background: #ccfbf1; padding: 2px 8px; border-radius: 9999px;">● New</span>')
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected messages as Read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as Unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
