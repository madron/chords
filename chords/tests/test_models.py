from django.test import TestCase
from . import factories


class SongTest(TestCase):
    def test_str(self):
        song = factories.SongFactory(title='Let it be')
        self.assertEqual(str(song), 'Let it be')

    def test_str_artist(self):
        song = factories.SongFactory(title='Let it be', artist='The Beatles')
        self.assertEqual(str(song), 'Let it be (The Beatles)')

    def test_get_data_title(self):
        song = factories.SongFactory(title='Let it be')
        self.assertEqual(song.get_data(), dict(title='Let it be'))

    def test_get_data_artist(self):
        song = factories.SongFactory(title='Let it be', artist='The Beatles')
        self.assertEqual(song.get_data(), dict(title='Let it be', artist='The Beatles'))

    def test_get_data_year(self):
        song = factories.SongFactory(title='Let it be', year=1970)
        self.assertEqual(song.get_data(), dict(title='Let it be', year=1970))

    def test_get_data_key(self):
        song = factories.SongFactory(title='Let it be', key='C')
        self.assertEqual(song.get_data(), dict(title='Let it be', key='C'))

    def test_get_data_chords(self):
        song = factories.SongFactory(title='Let it be', key='C', chords='{sov}\nWhen I [C]find myself in [G]times of trouble\n{eov}')
        self.assertEqual(song.get_data(), dict(title='Let it be', key='C', chords='{sov}\nWhen I [C]find myself in [G]times of trouble\n{eov}'))
