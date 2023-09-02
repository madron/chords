from django.test import TestCase
from django.urls import reverse

from . import factories


class TestMailerUserAdmin(TestCase):
    def setUp(self):
        factories.UserFactory(username='admin')
        self.assertTrue(self.client.login(username='admin', password='pass'))
        self.list = reverse('admin:auth_user_changelist')

    def test_list(self):
        response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:auth_user_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        user = factories.UserFactory(username='test1')
        url = reverse('admin:auth_user_change', args=(user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        user = factories.UserFactory(username='test2')
        url = reverse('admin:auth_user_delete', args=(user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
