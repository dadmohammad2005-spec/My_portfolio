from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from apps.contact.models import ContactMessage

class ContactTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_page_get(self):
        response = self.client.get(reverse('contact:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertContains(response, "Send a Message")

    def test_contact_form_valid_post(self):
        data = {
            'name': 'Sarah Connor',
            'email': 'sarah@example.com',
            'subject': 'Inquiry regarding project',
            'message': 'Hello, I loved your work on CloudScale and would like to hire you.',
            'website_hp': '', # Empty honeypot
        }
        response = self.client.post(reverse('contact:index'), data)
        self.assertEqual(response.status_code, 302) # Redirects on success

        # Verify message stored in DB
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Sarah Connor')

        # Verify email dispatched
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Sarah Connor', mail.outbox[0].subject)

    def test_contact_form_ajax_post(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Architecture Review',
            'message': 'Looking for an architect for a distributed API project.',
            'website_hp': '',
        }
        response = self.client.post(
            reverse('contact:index'),
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_contact_form_honeypot_spam_trap(self):
        # Spambot fills the hidden honeypot
        data = {
            'name': 'Spambot 9000',
            'email': 'spambot@spam.com',
            'subject': 'Buy crypto now',
            'message': 'Visit this spam link...',
            'website_hp': 'http://spamsite.com',
        }
        response = self.client.post(reverse('contact:index'), data)
        # Form should reject it and NOT create a ContactMessage
        self.assertEqual(ContactMessage.objects.count(), 0)
