from django.test import TestCase
from .. import utils


class GetSourceTest(TestCase):
    def test_title(self):
        data = dict(title='Let it be')
        lines = utils.get_source(data).splitlines()
        self.assertEqual(lines[0], '{title: Let it be}')
        self.assertEqual(lines[1], '')
        self.assertEqual(len(lines), 2)

    def test_artist(self):
        data = dict(title='Let it be', artist='The Beatles')
        lines = utils.get_source(data).splitlines()
        self.assertEqual(lines[0], '{title: Let it be}')
        self.assertEqual(lines[1], '{artist: The Beatles}')
        self.assertEqual(lines[2], '')
        self.assertEqual(len(lines), 3)

    def test_year(self):
        data = dict(title='Let it be', year=1970)
        lines = utils.get_source(data).splitlines()
        self.assertEqual(lines[0], '{title: Let it be}')
        self.assertEqual(lines[1], '{year: 1970}')
        self.assertEqual(lines[2], '')
        self.assertEqual(len(lines), 3)

    def test_key(self):
        data = dict(title='Let it be', key='C')
        lines = utils.get_source(data).splitlines()
        self.assertEqual(lines[0], '{title: Let it be}')
        self.assertEqual(lines[1], '{key: C}')
        self.assertEqual(lines[2], '')
        self.assertEqual(len(lines), 3)

    def test_chords(self):
        data = dict(title='Let it be', key='C', chords='{sov}\nWhen I [C]find myself in [G]times of trouble\n{eov}')
        lines = utils.get_source(data).splitlines()
        self.assertEqual(lines[0], '{title: Let it be}')
        self.assertEqual(lines[1], '{key: C}')
        self.assertEqual(lines[2], '')
        self.assertEqual(lines[3], '{sov}')
        self.assertEqual(lines[4], 'When I [C]find myself in [G]times of trouble')
        self.assertEqual(lines[5], '{eov}')
        self.assertEqual(len(lines), 6)

    def test_chords_only(self):
        data = dict(title='Let it be', key='C', chords='{sov}\nWhen I [C]find myself in [G]times of trouble\n{eov}')
        lines = utils.get_source(data, chords_only=True).splitlines()
        self.assertEqual(lines[0], '{sov}')
        self.assertEqual(lines[1], 'When I [C]find myself in [G]times of trouble')
        self.assertEqual(lines[2], '{eov}')
        self.assertEqual(len(lines), 3)


class GetSongFilenameTest(TestCase):
    def test_title(self):
        data = dict(title='Let it be')
        name = utils.get_song_filename(data, 'pdf')
        self.assertEqual(name, 'let-it-be.pdf')

    def test_artist(self):
        data = dict(artist='The Beatles')
        name = utils.get_song_filename(data, 'pdf')
        self.assertEqual(name, 'the-beatles.pdf')

    def test_artist_title(self):
        data = dict(artist='The Beatles', title='Let it be')
        name = utils.get_song_filename(data, 'pdf')
        self.assertEqual(name, 'the-beatles-let-it-be.pdf')

    def test_suffix(self):
        data = dict(artist='The Beatles', title='Let it be')
        name = utils.get_song_filename(data, 'pdf', suffix='chords')
        self.assertEqual(name, 'the-beatles-let-it-be-chords.pdf')


class GetChordproResultTest(TestCase):
    def test_ok(self):
        data = dict(title='Let it be', key='C', chords='{sov}\nXWhen I [C]find myself in [G]times of trouble\n{eov}')
        result, content = utils.get_chordpro_result(data)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, b'')
        self.assertEqual(result.stderr, b'')
        self.assertGreater(len(content), 1000)
