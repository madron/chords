from typing import Any, Dict
from django.db import models
from django.utils.translation import gettext_lazy as _
from . import constants


class Song(models.Model):
    title = models.CharField(_('title'), max_length=200, db_index=True)
    artist = models.CharField(_('artist'), max_length=200, blank=True, db_index=True)
    key = models.CharField(_('key'), max_length=50, blank=True)
    time = models.PositiveIntegerField(_('time'), blank=True, null=True, help_text=_('Beat per minute'))
    tempo = models.CharField(_('tempo'), max_length=50, blank=True, help_text=_('Signature. Eg. 4/4'))
    year = models.PositiveIntegerField(_('year'), blank=True, null=True, db_index=True)
    chords = models.TextField(_('chords'), blank=True, help_text=_('ChordPro format.'))

    class Meta:
        verbose_name = _('song')
        verbose_name_plural = _('songs')
        ordering = ['title']

    def __str__(self):
        if self.artist:
            return '{} ({})'.format(self.title, self.artist)
        return self.title

    def get_data(self) -> Dict[str, Any]:
        data = dict()
        for key in constants.ATTRIBUTES:
            value = getattr(self, key)
            if value:
                data[key] = value
        return data