from rest_framework import serializers
from apps.core.models import SiteSettings, Skill, Experience, Education
from apps.projects.models import Category, Project, ProjectScreenshot
from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'name', 'title', 'short_bio', 'detailed_bio', 'profile_photo',
            'resume_file', 'location', 'email', 'phone', 'github_url',
            'linkedin_url', 'twitter_url', 'is_available_for_hire',
            'hero_badge_text', 'years_of_experience', 'projects_completed',
            'satisfied_clients', 'meta_keywords', 'meta_description'
        ]


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'category_display', 'proficiency', 'icon', 'is_featured', 'order']


class ExperienceSerializer(serializers.ModelSerializer):
    tech_list = serializers.ListField(source='get_tech_list', read_only=True)

    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'role', 'location', 'employment_type',
            'start_date', 'end_date', 'is_current', 'description',
            'technologies', 'tech_list', 'order'
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'field_of_study', 'start_year', 'end_year', 'grade_or_honors', 'description', 'order']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProjectScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectScreenshot
        fields = ['id', 'image', 'caption', 'order']


class ProjectSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    tech_list = serializers.ListField(source='get_tech_list', read_only=True)
    screenshots = ProjectScreenshotSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'category', 'category_name', 'category_slug',
            'status', 'tagline', 'description', 'featured_image', 'technologies', 'tech_list',
            'github_url', 'live_demo_url', 'is_featured', 'order', 'screenshots', 'created_at'
        ]
        lookup_field = 'slug'


class BlogPostSerializer(serializers.ModelSerializer):
    tag_list = serializers.ListField(source='get_tag_list', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'category', 'tags', 'tag_list',
            'excerpt', 'content', 'cover_image', 'read_time', 'published_date'
        ]
        lookup_field = 'slug'


class ContactMessageSerializer(serializers.ModelSerializer):
    website_hp = serializers.CharField(required=False, write_only=True, allow_blank=True)

    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'website_hp', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_website_hp(self, value):
        if value:
            raise serializers.ValidationError("Bot submission rejected.")
        return value

    def create(self, validated_data):
        # Discard honeypot before model creation
        validated_data.pop('website_hp', None)
        return super().create(validated_data)
