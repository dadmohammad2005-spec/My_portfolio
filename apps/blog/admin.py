from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'read_time_badge', 'is_published', 'published_date')
    list_filter = ('is_published', 'category', 'published_date')
    list_editable = ('is_published',)
    search_fields = ('title', 'excerpt', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'

    fieldsets = (
        ("Header & Taxonomy", {
            "fields": ("title", "slug", "category", "tags", "cover_image")
        }),
        ("Content", {
            "fields": ("excerpt", "content")
        }),
        ("Publishing Metadata", {
            "fields": ("read_time", "is_published", "published_date")
        }),
    )

    def read_time_badge(self, obj):
        return f"{obj.read_time} min read"
    read_time_badge.short_description = "Read Time"
