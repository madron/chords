from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.utils.text import slugify
from django.views.generic import DetailView
from . import models


class SongPdfChordsView(PermissionRequiredMixin, DetailView):
    model = models.Song
    permission_required = 'chords.view_song'

    def render_to_response(self, context, **response_kwargs):
        song: models.Song = context['object']
        name = '{}-{}'.format(song.artist, song.title)
        filename = '{}.pdf'.format(slugify(name))
        content = 'to be done'
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
