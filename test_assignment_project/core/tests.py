from django.core.urlresolvers import reverse
from django.test import TestCase, Client

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
