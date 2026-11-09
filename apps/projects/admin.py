from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Project, ProjectScreenshot

class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ('image', 'caption', 'order', 'preview_thumbnail')
    readonly_fields = ('preview_thumbnail',)

    def preview_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; border-radius: 4px;" />', obj.image.url)
        return "No image"
    preview_thumbnail.short_description = "Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'project_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def project_count(self, obj):
        return obj.projects.count()
    project_count.short_description = "Total Projects"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'image_thumbnail', 'is_featured', 'order', 'created_at')
    list_filter = ('category', 'status', 'is_featured', 'created_at')
    list_editable = ('status', 'is_featured', 'order')
    search_fields = ('title', 'tagline', 'technologies', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectScreenshotInline]
    ordering = ('order', '-created_at')

    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "slug", "category", "status", "tagline", "featured_image")
        }),
        ("Content & Technologies", {
            "fields": ("technologies", "description")
        }),
        ("External Links", {
            "fields": ("github_url", "live_demo_url")
        }),
        ("Display Settings", {
            "fields": ("is_featured", "order")
        }),
    )

    def image_thumbnail(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 40px; border-radius: 4px;" />', obj.featured_image.url)
        return format_html('<span style="color: #94a3b8;">No Image</span>')
    image_thumbnail.short_description = "Thumbnail"
