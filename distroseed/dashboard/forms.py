from django import forms
# from django.forms import CheckboxSelectMultiple
from .models import *

class AutoTorrentForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Distro Name') 
    url = forms.URLField(label='URL to Scrape', initial='http://') 
    excludes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Excludes.objects.all())

    class Meta:
        model = AutoTorrent
        fields = ('name', 'url', 'excludes')
