from django.test import TestCase, Client
from django.urls import reverse
from apps.projects.models import Category, Project

class ProjectsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Full-Stack", slug="full-stack")
        self.project = Project.objects.create(
            title="Portfolio Platform",
            slug="portfolio-platform",
            category=self.category,
            tagline="A great production portfolio",
            description="Detailed breakdown of the portfolio architecture.",
            technologies="Django, React, PostgreSQL",
            github_url="https://github.com",
            is_featured=True
        )

    def test_project_list_view(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_list.html')
        self.assertContains(response, "Portfolio Platform")

    def test_project_list_filter_category(self):
        response = self.client.get(reverse('projects:list') + '?category=full-stack')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio Platform")

    def test_project_detail_view(self):
        response = self.client.get(reverse('projects:detail', kwargs={'slug': 'portfolio-platform'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_detail.html')
        self.assertContains(response, "A great production portfolio")

    def test_project_detail_404(self):
        response = self.client.get(reverse('projects:detail', kwargs={'slug': 'non-existent-slug'}))
        self.assertEqual(response.status_code, 404)
