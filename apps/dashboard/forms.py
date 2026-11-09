from django import forms
from django.contrib.auth.forms import AuthenticationForm
from apps.projects.models import Project, Category
from apps.blog.models import BlogPost
from apps.core.models import Skill, Experience, Education, SiteSettings


class StyledFormMixin:
    """Apply consistent portfolio dashboard styling classes to form widgets."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            current_classes = widget.attrs.get('class', '')
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs['class'] = f'{current_classes} form-checkbox'.strip()
            elif isinstance(widget, forms.Select):
                widget.attrs['class'] = f'{current_classes} form-select'.strip()
            elif isinstance(widget, forms.Textarea):
                widget.attrs['class'] = f'{current_classes} form-textarea'.strip()
            elif isinstance(widget, forms.FileInput):
                widget.attrs['class'] = f'{current_classes} form-file-input'.strip()
            else:
                widget.attrs['class'] = f'{current_classes} form-input'.strip()


class DashboardLoginForm(AuthenticationForm, StyledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Username or Email Address"
        self.fields['username'].widget.attrs.update({
            'placeholder': 'admin or your email',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Enter your password',
        })


class ProjectForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'category', 'tagline', 'description',
            'technologies', 'github_url', 'live_demo_url',
            'status', 'is_featured', 'order', 'featured_image'
        ]
        widgets = {
            'tagline': forms.TextInput(attrs={'placeholder': 'Catchy 1-2 sentence summary'}),
            'technologies': forms.TextInput(attrs={'placeholder': 'Django, PostgreSQL, React, Docker, AWS'}),
            'github_url': forms.URLInput(attrs={'placeholder': 'https://github.com/username/project'}),
            'live_demo_url': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Detailed case study, architecture, key features...'}),
        }


class BlogPostForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            'title', 'category', 'tags', 'read_time',
            'is_published', 'published_date', 'excerpt',
            'content', 'cover_image'
        ]
        widgets = {
            'category': forms.TextInput(attrs={'placeholder': 'e.g. Django, System Design, Cloud'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Python, Celery, Docker, Redis'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief teaser shown on blog cards...'}),
            'content': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Full article content (Markdown and HTML supported)...'}),
            'published_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class SkillForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'category', 'tier', 'proficiency', 'icon', 'is_featured', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Python, Django, PostgreSQL, Docker'}),
            'proficiency': forms.NumberInput(attrs={'min': 1, 'max': 100, 'step': 1}),
            'icon': forms.TextInput(attrs={'placeholder': 'code, server, database, cpu, etc.'}),
        }


class ExperienceForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            'company', 'role', 'location', 'employment_type',
            'start_date', 'end_date', 'is_current',
            'technologies', 'description', 'order'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'technologies': forms.TextInput(attrs={'placeholder': 'Python, Django, AWS, Kubernetes'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Key responsibilities, quantified achievements, impact...'}),
        }


class EducationForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            'institution', 'degree', 'field_of_study',
            'start_year', 'end_year', 'grade_or_honors',
            'description', 'order'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Relevant coursework, activities, honors...'}),
        }


class SiteSettingsForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'name', 'title', 'short_bio', 'detailed_bio',
            'profile_photo', 'resume_file', 'location',
            'email', 'phone', 'github_url', 'linkedin_url',
            'twitter_url', 'is_available_for_hire', 'hero_badge_text',
            'years_of_experience', 'projects_completed', 'satisfied_clients',
            'meta_keywords', 'meta_description'
        ]
        widgets = {
            'short_bio': forms.Textarea(attrs={'rows': 3}),
            'detailed_bio': forms.Textarea(attrs={'rows': 6}),
            'meta_description': forms.Textarea(attrs={'rows': 3}),
        }
