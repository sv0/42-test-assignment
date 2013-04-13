from django.conf import LazySettings
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
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

    def create_request(self):
        MyHttpRequest.objects.create(
            host='test.com',
            path='/path/',
            method='GET',
            remote_addr='8.8.8.8',
            is_secure=False,
            is_ajax=False,
            priority=choice(range(10))
        )

    def create_bunch_of_requests(self, number=10):
        for i in range(number):
            self.create_request()


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
        self.assertIsNot(response.context['request_list'], None)

    def test_order_requests_by_priority(self):
        for n in range(3):
            self.create_bunch_of_requests(n)
            response = self.client.get(reverse('first_requests'))
            context_request_list = response.context['request_list']
            request_priorities = [r.priority for r in context_request_list]
            request_priorities_sorted = request_priorities[:]
            request_priorities_sorted.sort()
            self.assertEqual(request_priorities, request_priorities_sorted)


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
    def setUp(self):
        self.user_content_type=ContentType.objects.get_for_model(User)

    def test_model_change_entry_delete(self):
        entries_before = ModelChangeEntry.objects.filter(
                            action_flag=DELETION,
                            content_type=self.user_content_type
                         ).count()
        # delete the first user
        User.objects.all()[0].delete()
        entries_after = ModelChangeEntry.objects.filter(
                            action_flag=DELETION).count()
        entries_diference = entries_after - entries_before
        self.assertEqual(entries_diference, 1)

    def test_model_change_entry_action_flag_and_content_type(self):
        user = User.objects.create_user(TEST_USERNAME,
                                        TEST_EMAIL,
                                        TEST_PASSWORD)
        latest_entry = ModelChangeEntry.objects.latest('id')
        self.assertEqual(latest_entry.action_flag, ADDITION)
        self.assertEqual(latest_entry.content_type, self.user_content_type)
        self.assertEqual(latest_entry.object_id, user.id)


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
