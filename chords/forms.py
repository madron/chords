from django import forms
from . import models


class SongForm(forms.ModelForm):
    class Meta:
        model = models.Song
        fields = '__all__'
        widgets = dict(
            title=forms.TextInput(attrs=dict(size=40)),
            artist=forms.TextInput(attrs=dict(size=40)),
            key=forms.TextInput(attrs=dict(size=10)),
            tempo=forms.TextInput(attrs=dict(size=10)),
            chords=forms.Textarea(attrs=dict(rows=70, cols=150)),
        )
