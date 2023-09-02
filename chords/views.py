from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views.generic import DetailView
from . import models
from . import utils


class SongSourceView(PermissionRequiredMixin, DetailView):
    model = models.Song
    permission_required = 'chords.view_song'

    def render_to_response(self, context, **response_kwargs):
        data = context['object'].get_data()
        filename = utils.get_song_filename(data, 'cho')
        content = utils.get_source(data)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


class SongPdfChordsView(PermissionRequiredMixin, DetailView):
    model = models.Song
    permission_required = 'chords.view_song'

    def render_to_response(self, context, **response_kwargs):
        data = context['object'].get_data()
        filename = utils.get_song_filename(data, 'pdf', suffix='chords')
        _, content = utils.get_chordpro_result(data, check=True)
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response


class SongPdfLyricsView(PermissionRequiredMixin, DetailView):
    model = models.Song
    permission_required = 'chords.view_song'

    def render_to_response(self, context, **response_kwargs):
        data = context['object'].get_data()
        filename = utils.get_song_filename(data, 'pdf', suffix='lyrics')
        _, content = utils.get_chordpro_result(data, check=True, lyrics_only=True)
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        return response
