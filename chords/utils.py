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
