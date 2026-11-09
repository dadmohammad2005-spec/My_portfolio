from django.test import TestCase, Client
from django.urls import reverse
from apps.blog.models import BlogPost

class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = BlogPost.objects.create(
            title="Deep Dive into Django 5",
            slug="deep-dive-into-django-5",
            category="Django",
            excerpt="An overview of Django 5 features",
            content="Full post content discussing features.",
            read_time=5,
            is_published=True
        )

    def test_blog_list_view(self):
        response = self.client.get(reverse('blog:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')
        self.assertContains(response, "Deep Dive into Django 5")

    def test_blog_detail_view(self):
        response = self.client.get(reverse('blog:detail', kwargs={'slug': 'deep-dive-into-django-5'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertContains(response, "Full post content discussing features.")
