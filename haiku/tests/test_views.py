from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from mock import patch, Mock

from haiku.models import Haiku
from django_lti_tool_provider.models import LtiUserData
from django_lti_tool_provider.signals import grade_updated_handler, _send_grade


class UserSetup(object):
    def setUp(self):
        self.password = 'some_password'
        self.user = get_user_model().objects.create(username='student_user')
        self.user.set_password(self.password)
        self.user.save()

        self.user2 = get_user_model().objects.create(username='student_user2')
        self.user2.set_password(self.password)
        self.user2.save()

    def login(self, username=None, password=None):
        username = username if username else self.user.username
        password = password if password else self.password
        self.assertTrue(self.client.login(username=username, password=password))


class HaikuHomeViewTestCase(UserSetup, TestCase):
    def setUp(self):
        super(HaikuHomeViewTestCase, self).setUp()
        self.home_url = reverse('haiku:home')

    def test_anonymous(self):
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('haiku:add'), 302)

    def test_no_haiku(self):
        self.login()
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('haiku:add'), 302)

    def test_one_haiku(self):
        haiku = Haiku.objects.create(poem='abc', author=self.user2)
        self.login()
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('haiku:add'), 302)

    def test_my_one_haiku(self):
        haiku = Haiku.objects.create(poem='abc', author=self.user)
        self.login()
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('haiku:view', kwargs=dict(pk=haiku.id)))

    def test_my_two_haiku(self):
        Haiku.objects.create(poem='abc', author=self.user)
        Haiku.objects.create(poem='def', author=self.user)
        self.login()
        response = self.client.get(self.home_url)
        self.assertRedirects(response, reverse('haiku:list'))


class HaikuCreateViewTestCase(UserSetup, TestCase):
    def setUp(self):
        super(HaikuCreateViewTestCase, self).setUp()
        self.add_url = reverse('haiku:add')

    def test_anonymous(self):
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.add_url)
        login_url = ''.join([reverse('admin:login'), '?next=', self.add_url])
        self.assertRedirects(response, login_url)

    def test_invalid(self):
        self.login()
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.add_url)
        self.assertEqual(response.status_code, 200)

    def test_valid(self):
        self.login()
        response = self.client.get(self.add_url)
        self.assertEqual(response.status_code, 200)

        post_data = {'poem': '123'}
        response = self.client.post(self.add_url, post_data)
        haiku = Haiku.objects.order_by('-id')[0]
        self.assertRedirects(response, reverse('haiku:view', kwargs=dict(pk=haiku.id)))


class HaikuUpdateViewTestCase(UserSetup, TestCase):
    def setUp(self):
        super(HaikuUpdateViewTestCase, self).setUp()
        self.haiku = Haiku.objects.create(poem='abc', author=self.user)
        self.view_url = reverse('haiku:view', kwargs=dict(pk=self.haiku.id))
        self.edit_url = reverse('haiku:edit', kwargs=dict(pk=self.haiku.id))
        self.login_url = ''.join([reverse('admin:login'), '?next=', self.edit_url])

    def test_anonymous(self):
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.edit_url)
        self.assertRedirects(response, self.login_url)

    def test_invalid(self):
        self.login(self.user2.username)
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.edit_url)
        self.assertEquals(response.status_code, 403)

    def test_valid(self):
        self.login()
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)

        post_data = {'poem': '123'}
        response = self.client.post(self.edit_url, post_data)
        self.assertRedirects(response, self.view_url)
        response = self.client.get(self.view_url)
        self.assertEquals(response.context['object'].poem, post_data['poem'])
