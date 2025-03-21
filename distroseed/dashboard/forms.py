from django import forms
from .models import *

class AutoTorrentForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    name = forms.CharField(max_length=200, label='Distro Name') 
    url = forms.URLField(label='URL to Scrape', initial='http://') 
    excludes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Excludes.objects.all(), required=False)
    includes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Includes.objects.all(), required=False)
    error_messages={
        'unique':"This distro already exist. Either choose a different name or edit the current one."
    }

    class Meta:
        model = AutoTorrent
        fields = ('id', 'name', 'url', 'excludes', 'includes')
    


class NewAutoTorrentForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Distro Name') 
    url = forms.URLField(label='URL to Scrape', initial='http://') 
    excludes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Excludes.objects.all(), required=False)
    includes = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Includes.objects.all(), required=False)
    error_messages={
        'unique':"This distro already exist. Either choose a different name or edit the current one."
    }

    class Meta:
        model = AutoTorrent
        fields = ('name', 'url', 'excludes', 'includes')

class TransmissionSettingForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = TransmissionSetting
        fields = ('__all__')

class ExcludesForm(forms.ModelForm):
    class Meta:
        model = Excludes
        fields = ['phrase']
        widgets = {
            'phrase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter exclusion phrase'}),
        }
        labels = {
            'phrase': 'Exclusion Phrase',
        }

class IncludesForm(forms.ModelForm):
    class Meta:
        model = Includes
        fields = ['phrase']
        widgets = {
            'phrase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter inclusion phrase'}),
        }
        labels = {
            'phrase': 'Inclusion Phrase',
        }

class DeletePhraseForm(forms.Form):
    phrase_id = forms.IntegerField(widget=forms.HiddenInput())