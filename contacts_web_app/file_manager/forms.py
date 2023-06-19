from django.forms import ModelForm, TextInput, ClearableFileInput

from .models import Picture, Document, Video, Audio, Archive


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['title', 'image']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'image': ClearableFileInput(attrs={'class': 'form-control-file'})}


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'document': ClearableFileInput(attrs={'class': 'form-control-file'})}


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'video': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class AudioForm(ModelForm):
    class Meta:
        model = Audio
        fields = ['artist', 'title', 'audio']
        widgets = {
            'artist': TextInput(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'audio': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class ArchiveForm(ModelForm):
    class Meta:
        model = Archive
        fields = ['title', 'archive']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'archive': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
