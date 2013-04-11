from django.conf import LazySettings
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.core import management
from django.core.urlresolvers import reverse
from django.template import Template, Context
from django.test import TestCase, Client
from random import choice
from models import MyHttpRequest, ModelChangeEntry
from forms import ProfileChangeForm
from management.commands.project_models import get_project_models
from cStringIO import StringIO
import sys


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

    def test_context(self):
        """
        Tests that response context contains settings.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['settings'], LazySettings)

    def test_get_contacts_form_anon(self):
        response = self.client.get(reverse('edit_contacts'))
        self.assertEqual(response.status_code, 302)

    def test_get_contacts_form_auth(self):
        User.objects.create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        response = self.client.get(reverse('edit_contacts'))
        self.assertEqual(response.status_code, 200)

    def test_post_contacts_form_auth(self, **kwargs):
        User.objects.create_user(TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD)
        self.client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
        user = User.objects.get(pk=2)  # get sv user
        requested_with = 'XMLHttpRequest' if kwargs.get('is_ajax') else ''
        response = self.client.post(reverse('edit_contacts'), TEST_FORM_DATA,
                                    HTTP_X_REQUESTED_WITH=requested_with)
        self.assertIn(response.status_code, (200, 302))
        response = self.client.get(reverse('home'))
        self.assertContains(response, TEST_FORM_DATA.get('first_name'))
        self.assertContains(response, TEST_FORM_DATA.get('last_name'))

    def test_ajax_contacts_form_auth(self):
        self.test_post_contacts_form_auth(is_ajax=True)


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


class TemplateTagTest(TestCase):
    def setUp(self):
        template = "{% load core_tags %}{% edit_link obj %}"
        self.template = Template(template)

    def test_edit_link_tag(self):
        user = choice(list(User.objects.all()))
        c = Context({'obj': user})
        self.assertIn('/auth/user/%s/' % user.id, self.template.render(c))

    def test_edit_link_tag_not_django_model(self):
        # choice random object from the list
        obj = choice((u'unicode string', 100500, LazySettings()))
        c = Context({'obj': obj})
        self.assertEqual('', self.template.render(c))


class TestProjectModelsCount(TestCase):
    def setUp(self):
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        self.random_project_model_name = choice(list(get_project_models()))[0]

    def test_get_project_models(self):
        self.assertIsNot(list(get_project_models()), [])

    def test_project_models_stdout(self):
        management.call_command('project_models')
        out = sys.stdout.getvalue()
        self.assertIn(self.random_project_model_name, out)

    def test_project_models_stderr(self):
        management.call_command('project_models')
        err = sys.stderr.getvalue()
        self.assertIn("error: %s" % self.random_project_model_name, err)


class TestModelChangeEntry(TestCase):
    def test_model_change_entry_count(self):
        entries_before = ModelChangeEntry.objects.filter(
                            action_flag=DELETION).count()
        User.objects.all().delete()
        entries_after = ModelChangeEntry.objects.filter(
                            action_flag=DELETION).count()
        self.assertGreater(entries_after, entries_before)


class TestProfileChangeForm(TestCase):
    def test_profile_change_form_good(self):
        user = User.objects.get(pk=2)
        form = ProfileChangeForm(TEST_FORM_DATA, instance=user)
        self.assertTrue(form.is_valid())

    def test_profile_change_form_bad(self):
        user = choice(list(User.objects.all()))
        form = ProfileChangeForm({'first_name': 'fake',
                                  'last_name': u'fake'},
                                  instance=user)
        self.assertFalse(form.is_valid())
