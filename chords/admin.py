from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from . import forms
from . import models
from . import views


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'pdf_chords_link', 'key', 'time', 'tempo', 'year']
    list_filter = ['artist']
    search_fields = ['title', 'artist']
    fields = [
        ('title', 'artist'),
        ('key', 'time', 'tempo', 'year'),
        'chords',
    ]
    form = forms.SongForm

    class Media:
        css = dict(all=['fontawesomefree/css/all.min.css'])

    def get_url_name(self, name):
        info = dict(app_label=self.model._meta.app_label, model_name=self.model._meta.model_name, name=name)
        return '{app_label}_{model_name}_{name}'.format(**info)

    def get_urls(self):
        urls = [
            path('<slug:pk>/pdf/chords/',
                self.admin_site.admin_view(views.SongPdfChordsView.as_view()),
                name=self.get_url_name('pdf_chords')
            ),
        ]
        return urls + super().get_urls()

    def pdf_chords_link(self, obj):
        name = 'admin:{}'.format(self.get_url_name('pdf_chords'))
        url = reverse(name, args=(obj.pk,))
        icon = '<i class="fa-regular fa-file-pdf fa-lg"></i>'
        return format_html('<a href="{}">{}</a>', url, mark_safe(icon))
    pdf_chords_link.short_description = _('chords')
