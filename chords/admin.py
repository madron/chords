from django.contrib import admin
from . import forms
from . import models


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'key', 'time', 'tempo', 'year']
    list_filter = ['artist']
    search_fields = ['title', 'artist']
    form = forms.SongForm
