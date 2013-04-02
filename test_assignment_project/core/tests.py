from django.conf import LazySettings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from models import MyHttpRequest
from forms import ProfileChangeForm

TEST_USERNAME = 'fake'
TEST_PASSWORD = 'fake'
TEST_EMAIL = 'fake@example.com'

TEST_FORM_DATA = {
    'first_name': 'fake',
    'last_name': u'fake',
    'date_of_birth': '1961-04-12',
    'email': u'fake@example.com',
}


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
