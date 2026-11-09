from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import logging

from apps.core.models import SiteSettings, Skill, Experience, Education
from apps.projects.models import Category, Project
from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage
from .serializers import (
    SiteSettingsSerializer, SkillSerializer, ExperienceSerializer,
    EducationSerializer, CategorySerializer, ProjectSerializer,
    BlogPostSerializer, ContactMessageSerializer
)

logger = logging.getLogger(__name__)

class SiteSettingsAPIView(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        return SiteSettings.load()


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category=category)
        return qs


class ExperienceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class EducationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.select_related('category').prefetch_related('screenshots').all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        category_slug = self.request.query_params.get('category')
        is_featured = self.request.query_params.get('featured')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if is_featured:
            qs = qs.filter(is_featured=True)
        return qs


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(is_published=True)
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class ContactCreateAPIView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Save client IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        instance = serializer.save(ip_address=ip)

        # Send email notification
        try:
            subject_line = f"New Portfolio Inquiry: {instance.subject} from {instance.name}"
            email_body = (
                f"You received a new message from your portfolio contact form:\n\n"
                f"Name: {instance.name}\n"
                f"Email: {instance.email}\n"
                f"Subject: {instance.subject}\n"
                f"IP: {ip}\n\n"
                f"Message:\n{instance.message}\n"
            )
            send_mail(
                subject=subject_line,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                fail_silently=True,
            )
        except Exception as e:
            logger.warning(f"Could not send email notification for contact message: {e}")
