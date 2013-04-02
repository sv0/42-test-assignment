from django.conf import LazySettings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase, Client
from random import choice
from models import MyHttpRequest


class ContactTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        """
        Tests that home page contains required information.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Name')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Skype')
        self.assertContains(response, 'Bio')

    def test_context(self):
        """
        Tests that response context contains settings.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['settings'], LazySettings)


class MyHttpRequestTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_request(self):
        """
        Tests that MyHttpRequest item exists in the database
        after GET was handlled
        """
        url = reverse('home')
        self.client.get(url)
        self.assertTrue(MyHttpRequest.objects.filter(path=url).exists())

    def test_first_requests_view(self):
        """
        Tests that first_requests view works correctly.
        """
        response = self.client.get(reverse('first_requests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'List of the first')
