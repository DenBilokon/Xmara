from django.forms import ModelForm, TextInput, ClearableFileInput

from .models import Picture, Document, Video, Audio


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
        fields = ['title', 'audio']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'audio': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
