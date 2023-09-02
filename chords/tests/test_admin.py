from django.test import TestCase
from django.urls import reverse
from authentication.tests.factories import UserFactory
from . import factories


class SongAdminTest(TestCase):
    def setUp(self):
        UserFactory(username='admin')
        self.assertTrue(self.client.login(username='admin', password='pass'))
        self.list = reverse('admin:chords_song_changelist')

    def test_list(self):
        with self.assertNumQueries(6):
            response = self.client.get(self.list)
        self.assertEqual(response.status_code, 200)
        for _ in range(5):
            song = factories.SongFactory()
        with self.assertNumQueries(6):
            response = self.client.get(self.list)

    def test_search(self):
        data = dict(q='text')
        response = self.client.get(self.list, data)
        self.assertEqual(response.status_code, 200)

    def test_add(self):
        url = reverse('admin:chords_song_add')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail(self):
        shipment = factories.SongFactory()
        url = reverse('admin:chords_song_change', args=(shipment.pk,))
        with self.assertNumQueries(5):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        with self.assertNumQueries(5):
            response = self.client.get(url)

    def test_delete(self):
        shipment = factories.SongFactory()
        url = reverse('admin:chords_song_delete', args=(shipment.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

