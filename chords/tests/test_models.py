from django.test import TestCase
from . import factories


class SongTest(TestCase):
    def test_str(self):
        song = factories.SongFactory(title='Let it be')
        self.assertEqual(str(song), 'Let it be')

    def test_str_artist(self):
        song = factories.SongFactory(title='Let it be', artist='The Beatles')
        self.assertEqual(str(song), 'Let it be (The Beatles)')
