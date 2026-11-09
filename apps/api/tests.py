from django.test import TestCase
from rest_framework.test import APIClient
from apps.core.models import SiteSettings, Skill
from apps.projects.models import Project, Category
from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.settings_obj = SiteSettings.load()
        self.category = Category.objects.create(name="Cloud", slug="cloud")
        self.project = Project.objects.create(
            title="Cloud Project",
            slug="cloud-project",
            category=self.category,
            tagline="Tagline here",
            description="Description here",
            technologies="Django, Docker"
        )
        self.skill = Skill.objects.create(name="Django", proficiency=95)
        self.post = BlogPost.objects.create(
            title="API Post",
            slug="api-post",
            excerpt="Post excerpt",
            content="Content"
        )

    def test_get_settings_api(self):
        response = self.client.get('/api/settings/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.settings_obj.name)

    def test_get_projects_api(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        # Check paginated results
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['slug'], 'cloud-project')

    def test_get_project_detail_api(self):
        response = self.client.get('/api/projects/cloud-project/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Cloud Project')

    def test_get_skills_api(self):
        response = self.client.get('/api/skills/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_post_contact_api(self):
        data = {
            'name': 'API Tester',
            'email': 'tester@api.com',
            'subject': 'Testing API contact endpoint',
            'message': 'Testing message from external consumer.',
            'website_hp': ''
        }
        response = self.client.post('/api/contact/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ContactMessage.objects.filter(email='tester@api.com').count(), 1)

    def test_post_contact_api_bot_rejection(self):
        data = {
            'name': 'API Bot',
            'email': 'bot@spam.com',
            'subject': 'Spam subject',
            'message': 'Spam message',
            'website_hp': 'bot_data_here'
        }
        response = self.client.post('/api/contact/', data)
        self.assertEqual(response.status_code, 400)
