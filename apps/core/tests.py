from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import SiteSettings, Skill, Experience, Education
from apps.projects.models import Project, Category
import datetime

class CoreViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.settings_obj = SiteSettings.load()
        self.settings_obj.name = "Dad Mohammad"
        self.settings_obj.save()

        self.skill = Skill.objects.create(
            name="Python",
            category="backend",
            proficiency=95,
            is_featured=True,
            order=1
        )
        self.exp = Experience.objects.create(
            company="Tech Corp",
            role="Backend Dev",
            location="Remote",
            start_date=datetime.date(2022, 1, 1),
            is_current=True,
            description="Built APIs",
            technologies="Django, Docker"
        )
        self.edu = Education.objects.create(
            institution="University of Tech",
            degree="B.S.",
            field_of_study="CS",
            start_year=2018,
            end_year=2022
        )

    def test_home_page_status_and_content(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dad Mohammad")
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('featured_skills', response.context)

    def test_about_page_status_and_content(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
        self.assertIn('skills_by_category', response.context)
        self.assertIn('experiences', response.context)
        self.assertIn('educations', response.context)
        self.assertContains(response, "Tech Corp")

    def test_resume_view_status(self):
        response = self.client.get(reverse('core:resume'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'resume.html')
        self.assertContains(response, "Professional Resume")

    def test_careers_view_status_and_content(self):
        response = self.client.get(reverse('core:careers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'careers.html')
        self.assertContains(response, "Career Opportunities")
        self.assertIn('contact_form', response.context)
        self.assertIn('experiences', response.context)

    def test_scholarships_view_status_and_content(self):
        response = self.client.get(reverse('core:scholarships'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'scholarships.html')
        self.assertContains(response, "Graduate Studies &amp; Scholarships")
        self.assertIn('educations', response.context)
        self.assertIn('academic_projects' if 'academic_projects' in response.context else 'projects', response.context)
