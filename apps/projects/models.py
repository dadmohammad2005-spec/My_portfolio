from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    tagline = models.CharField(
        max_length=300,
        help_text="Catchy 1-2 sentence summary for project cards"
    )
    description = models.TextField(
        help_text="Detailed project breakdown, architecture, challenges solved, and key features"
    )
    featured_image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Hero image for the project card and header"
    )
    technologies = models.CharField(
        max_length=255,
        help_text="Comma-separated technologies (e.g. Django, React, PostgreSQL, Docker, AWS)"
    )
    github_url = models.URLField(blank=True, help_text="Link to public or private repository")
    live_demo_url = models.URLField(blank=True, help_text="Live URL to test application")
    STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('experimental', 'Experimental'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='completed',
        help_text="Project status: completed, in_progress, or experimental"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Pin to the Home page featured projects section"
    )
    order = models.PositiveIntegerField(default=0, help_text="Ordering display sequence")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def get_tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='screenshots'
    )
    image = models.ImageField(upload_to='projects/screenshots/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Project Screenshot"
        verbose_name_plural = "Project Screenshots"

    def __str__(self):
        return f"Screenshot for {self.project.title} ({self.caption or 'No caption'})"
