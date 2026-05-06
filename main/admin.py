from django.contrib import admin
from .models import About, Skill, Project, ContactMessage

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'location']
    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'title', 'bio', 'email', 'phone', 'location', 'profile_image')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin')
        }),
        ('CV', {
            'fields': ('cv_file',)
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'percentage']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'github_link', 'live_link']
    list_filter = ['created_at']
    search_fields = ['title', 'technologies']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"