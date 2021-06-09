from django import forms
from django.forms import fields
from .models import Album,Song


class SongForm(forms.ModelForm):
    class Meta:
        model=Song
        fields=['song_title','audio_file']