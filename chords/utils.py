import subprocess
import tempfile
from typing import Any, Dict
from django.utils.text import slugify
from . import constants


def get_source(data: Dict[str, Any])-> str:
    directives = []
    for key in constants.DIRECTIVES:
        value = data.get(key, None)
        if value:
            directives.append('{{{}: {}}}'.format(key, value))
    directives.append('')
    preamble = '\n'.join(directives)
    chords = data.get('chords', '')
    return '{}\n{}'.format(preamble, chords)


def get_song_filename(data: Dict[str, Any], extension: str, suffix: str='')-> str:
    parts = [
        data.get('artist', None),
        data.get('title', None),
    ]
    slug = slugify('-'.join([x for x in parts if x]))
    if suffix:
        return '{}-{}.{}'.format(slug, suffix, extension)
    return '{}.{}'.format(slug, extension)


def get_chordpro_result(data: Dict[str, Any], check: bool=False, lyrics_only: bool=False):
    source = get_source(data)
    source_file = tempfile.NamedTemporaryFile(mode='w')
    output_file = tempfile.NamedTemporaryFile(mode='rb')
    source_file.write(source)
    source_file.seek(0)
    command = 'chordpro -o {} {}'.format(output_file.name, source_file.name)
    if lyrics_only:
        command = ' '.join(command, '--lyrics-only')
    result = subprocess.run([command], shell=True, capture_output=True, check=check)
    source_file.close()
    output_file.seek(0)
    content = output_file.read()
    output_file.close()
    return result, content
