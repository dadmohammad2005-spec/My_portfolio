from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Skill, Experience, Education, Certification

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Personal Identity", {
            "fields": ("name", "title", "profile_photo", "short_bio", "detailed_bio")
        }),
        ("Contact & Location", {
            "fields": ("email", "phone", "location")
        }),
        ("Social Links", {
            "fields": ("github_url", "linkedin_url", "twitter_url")
        }),
        ("Resume & Availability", {
            "fields": ("resume_file", "is_available_for_hire", "hero_badge_text")
        }),
        ("Key Statistics", {
            "fields": ("years_of_experience", "projects_completed", "satisfied_clients")
        }),
        ("SEO Meta Tags", {
            "fields": ("meta_keywords", "meta_description")
        }),
    )

    def has_add_permission(self, request):
        # Prevent adding multiple instances of singleton
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'tier', 'is_featured', 'order')
    list_filter = ('category', 'tier', 'is_featured')
    list_editable = ('tier', 'is_featured', 'order')
    search_fields = ('name',)
    ordering = ('order', 'name')

    def proficiency_bar(self, obj):
        return format_html(
            '''
            <div style="background-color: #e2e8f0; width: 120px; border-radius: 4px; overflow: hidden; display: inline-block; vertical-align: middle;">
                <div style="background-color: #0d9488; width: {}%; height: 12px;"></div>
            </div>
            <span style="margin-left: 8px; font-weight: 600;">{}%</span>
            ''',
            obj.proficiency,
            obj.proficiency
        )
    proficiency_bar.short_description = "Proficiency"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company', 'location', 'start_date', 'end_date', 'is_current', 'order')
    list_filter = ('is_current', 'employment_type')
    list_editable = ('order',)
    search_fields = ('role', 'company', 'description', 'technologies')
    ordering = ('order', '-start_date')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'field_of_study', 'institution', 'start_year', 'end_year', 'order')
    list_editable = ('order',)
    search_fields = ('degree', 'field_of_study', 'institution')
    ordering = ('order', '-start_year')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'issue_date', 'credential_id', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'issuer', 'credential_id', 'description')
    ordering = ('order', 'title')

