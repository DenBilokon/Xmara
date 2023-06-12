from django.forms import ModelForm, TextInput, ClearableFileInput, Form, FileField

from .models import Picture, Document, Video


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['title', 'description', 'image']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'image': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


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
