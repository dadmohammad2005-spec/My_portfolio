from django.db import models
from django.utils import timezone

class About(models.Model):
    name = models.CharField(max_length=100, default='Dad Mohammad')
    title = models.CharField(max_length=200, default='Full Stack Django Developer')
    bio = models.TextField(default='I build professional web applications using Python & Django.')
    email = models.EmailField(default='dad@example.com')
    phone = models.CharField(max_length=20, default='+92 XXX XXXXXXX')
    location = models.CharField(max_length=100, default='Pakistan')
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    cv_file = models.FileField(upload_to='cv/', blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'About'

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Tools & DevOps'),
    ]
    
    name = models.CharField(max_length=50)
    percentage = models.IntegerField(default=0)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return f"{self.name} - {self.category}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=200, help_text='e.g., Python, Django, Bootstrap')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']