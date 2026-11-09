from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class SiteSettings(models.Model):
    """
    Singleton model to manage portfolio owner information,
    social links, hero content, SEO metadata, and resume.
    """
    name = models.CharField(max_length=120, default="Dad Mohammad", help_text="Full Name displayed on the site")
    title = models.CharField(max_length=200, default="Software Engineer", help_text="Professional headline")
    short_bio = models.TextField(
        default="I build resilient, high-performance web applications and cloud architectures with Python, Django, modern JavaScript, and distributed systems.",
        help_text="2-3 lines for the Hero section"
    )
    detailed_bio = models.TextField(
        default="I am a passionate software engineer with 5+ years of experience designing scalable backends and crisp, responsive frontend interfaces. I specialize in Django, RESTful APIs, modern databases, and clean architecture.",
        help_text="Full bio for the About page"
    )
    profile_photo = models.ImageField(upload_to='profile/', blank=True, null=True, help_text="Upload square avatar or photo")
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True, help_text="Upload your resume (PDF recommended)")
    
    # Location & Contact
    location = models.CharField(max_length=150, default="San Francisco, CA")
    email = models.EmailField(default="dadmohammad.dev@example.com")
    phone = models.CharField(max_length=50, blank=True, default="+1 (555) 019-2834")
    
    # Social Links
    github_url = models.URLField(default="https://github.com")
    linkedin_url = models.URLField(default="https://linkedin.com")
    twitter_url = models.URLField(blank=True, default="https://twitter.com")
    
    # Hero & Stats
    is_available_for_hire = models.BooleanField(default=True)
    hero_badge_text = models.CharField(max_length=150, default="Available for new opportunities")
    years_of_experience = models.PositiveIntegerField(default=5)
    projects_completed = models.PositiveIntegerField(default=20)
    satisfied_clients = models.PositiveIntegerField(default=15)
    
    # SEO
    meta_keywords = models.CharField(max_length=255, default="Dad Mohammad, Software Engineer, Python, Django, REST API, Portfolio")
    meta_description = models.TextField(
        default="Personal portfolio of Dad Mohammad - Software Engineer specializing in Python, Django, and modern web architectures."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"Portfolio Settings: {self.name}"

    def save(self, *args, **kwargs):
        # Enforce singleton pattern: only one instance allowed
        if not self.pk and SiteSettings.objects.exists():
            self.pk = SiteSettings.objects.first().pk
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('backend', 'Backend Development & APIs'),
        ('database', 'Databases & ORM'),
        ('tools', 'Developer Tools & Workflows'),
        ('ai', 'AI & Intelligent Systems'),
        ('frontend', 'Frontend & Modern UI'),
    ]

    TIER_CHOICES = [
        ('proficient', 'Proficient'),
        ('working', 'Working Knowledge'),
        ('learning', 'Currently Learning'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='backend')
    tier = models.CharField(max_length=30, choices=TIER_CHOICES, default='proficient', help_text="Recruiter competence tier")
    proficiency = models.PositiveIntegerField(
        default=85,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Internal proficiency ranking between 1 and 100"
    )
    icon = models.CharField(max_length=60, blank=True, help_text="Lucide icon name (e.g., code, server, database, cpu)")
    is_featured = models.BooleanField(default=True, help_text="Display prominently on the Home hero section")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} [{self.get_tier_display()}]"


class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=150, default="Remote")
    employment_type = models.CharField(max_length=80, default="Full-Time")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if currently working here")
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="Key achievements, impact, and responsibilities (Markdown or line breaks supported)")
    technologies = models.CharField(max_length=255, blank=True, help_text="Comma-separated technologies used (e.g. Django, PostgreSQL, Docker)")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"

    def __str__(self):
        return f"{self.role} at {self.company}"

    def get_tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField(default=2016)
    end_year = models.PositiveIntegerField(blank=True, null=True, default=2020)
    grade_or_honors = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_year']
        verbose_name = "Education"
        verbose_name_plural = "Education Records"

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} - {self.institution}"


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150)
    issue_date = models.CharField(max_length=80, default="Jul 2026")
    credential_id = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True, default="https://coursera.org/verify")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"

    def __str__(self):
        return f"{self.title} - {self.issuer}"

