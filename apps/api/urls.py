from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SiteSettingsAPIView, SkillViewSet, ExperienceViewSet,
    EducationViewSet, CategoryViewSet, ProjectViewSet,
    BlogPostViewSet, ContactCreateAPIView
)

router = DefaultRouter()
router.register(r'skills', SkillViewSet, basename='api-skills')
router.register(r'experience', ExperienceViewSet, basename='api-experience')
router.register(r'education', EducationViewSet, basename='api-education')
router.register(r'categories', CategoryViewSet, basename='api-categories')
router.register(r'projects', ProjectViewSet, basename='api-projects')
router.register(r'blog', BlogPostViewSet, basename='api-blog')

urlpatterns = [
    path('settings/', SiteSettingsAPIView.as_view(), name='api-settings'),
    path('contact/', ContactCreateAPIView.as_view(), name='api-contact'),
    path('', include(router.urls)),
]
