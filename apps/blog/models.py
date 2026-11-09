from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

class BlogPost(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=80, default="Engineering", help_text="e.g. Django, Architecture, Cloud, Frontend")
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags (e.g. Python, Docker, API)")
    excerpt = models.TextField(help_text="2-3 sentence overview displayed on article cards")
    content = models.TextField(help_text="Full post content (HTML or Markdown supported)")
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    read_time = models.PositiveIntegerField(default=5, help_text="Estimated reading time in minutes")
    is_published = models.BooleanField(default=True)
    published_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    def get_tag_list(self):
        if not self.tags:
            return []
        return [t.strip() for t in self.tags.split(',') if t.strip()]
