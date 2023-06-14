from django.forms import ModelForm, TextInput, ClearableFileInput

from .models import Library


class LibraryForm(ModelForm):
    class Meta:
        model = Library
        fields = ['title', 'description', 'image']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'image': ClearableFileInput(attrs={'class': 'form-control-file'}),
        }