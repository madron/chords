import subprocess
import tempfile
from typing import Any, Dict, Tuple
from django.utils.html import format_html_join
from django.utils.text import slugify
from . import constants


def get_source(data: Dict[str, Any], chords_only: bool = False)-> str:
    directives = []
    if chords_only:
        directives.append('{{title: {}}}'.format(data.get('title', '')))
    else:
        for key in constants.DIRECTIVES:
            value = data.get(key, None)
            if value:
                directives.append('{{{}: {}}}'.format(key, value))
        directives.append('')
        directives.append('')
    preamble = '\n'.join(directives)
    chords = data.get('chords', '')
    return '{}{}'.format(preamble, chords)


def get_song_filename(data: Dict[str, Any], extension: str, suffix: str='')-> str:
    parts = [
        data.get('artist', None),
        data.get('title', None),
    ]
    slug = slugify('-'.join([x for x in parts if x]))
    if suffix:
        return '{}-{}.{}'.format(slug, suffix, extension)
    return '{}.{}'.format(slug, extension)


def get_chordpro_result(
        data: Dict[str, Any],
        check: bool=False,
        lyrics_only: bool=False,
        source_only: bool=False,
    ) -> Tuple[subprocess.CompletedProcess, bytes]:
    source = get_source(data, chords_only=source_only)
    source_file = tempfile.NamedTemporaryFile(mode='w')
    output_file = tempfile.NamedTemporaryFile(mode='rb')
    source_file.write(source)
    source_file.seek(0)
    command = 'chordpro -o {} {}'.format(output_file.name, source_file.name)
    if lyrics_only:
        command = ' '.join([command, '--lyrics-only'])
    result = subprocess.run([command], shell=True, capture_output=True, check=check)
    source_file.close()
    output_file.seek(0)
    content = output_file.read()
    output_file.close()
    return result, content


def format_html_from_bytes(data: bytes):
    text = data.decode('utf-8')
    return format_html_join("", "{}<br>", [(l,) for l in text.splitlines()])
