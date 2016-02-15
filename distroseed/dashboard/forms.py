from django import forms
from .models import *

class AutoTorrentForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField(max_length=200, label='Distro Name') 
    url = forms.URLField(label='URL to Scrape', initial='http://') 
    excludes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Excludes.objects.all())
    error_messages={
        'unique':"This distro already exist. Either choose a different name or edit the current one."
    }

    class Meta:
        model = AutoTorrent
        fields = ('id', 'name', 'url', 'excludes')

class NewAutoTorrentForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Distro Name') 
    url = forms.URLField(label='URL to Scrape', initial='http://') 
    excludes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Excludes.objects.all())
    error_messages={
        'unique':"This distro already exist. Either choose a different name or edit the current one."
    }

    class Meta:
        model = AutoTorrent
        fields = ('name', 'url', 'excludes')

class TransmissionSettingForm(forms.ModelForm):
    class Meta:
        model = TransmissionSetting
        fields = ('__all__')
