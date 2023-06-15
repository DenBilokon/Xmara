import requests

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Picture, Document, Video, Audio
from .forms import PictureForm, DocumentForm, VideoForm, AudioForm


@login_required
def main_mf(request):
    return render(request, 'file_manager/index.html', context={})


def upload_picture(request):
    user_id = request.user.id
    cloud_images = Picture.objects.filter(user_id=user_id)
    image_form = PictureForm()
    # image_form = dict(backend_form=PictureForm())

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        # image_form['posted'] = form.instance
        if form.is_valid():
            form.save()
            return redirect('file_manager:upload_picture')

    context = {
        'cloud_images': cloud_images,
        'image_form': image_form
    }
    return render(request, 'file_manager/upload_picture.html', context=context)


def download_image(request, image_url):
    response = requests.get(image_url)
    content_type = response.headers.get('content-type')
    filename = image_url.split('/')[-1]  # Отримати назву файлу з URL
    print(filename)

    # Налаштувати заголовки відповіді для завантаження файлу
    response = HttpResponse(response.content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def upload_video(request):
    user_id = request.user.id
    cloud_video = Video.objects.filter(user_id=user_id)
    video_form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        # video_form['posted'] = form.instance
        if form.is_valid():
            form.save()
            return redirect('file_manager:upload_video')
        elif Exception:
            return render(request, "file_manager/upload_video.html",
                          context={'form': VideoForm(), "message": "Form not valid"})

    context = {
        'cloud_video': cloud_video,
        'video_form': video_form,
    }
    return render(request, 'file_manager/upload_video.html', context=context)


def upload_document(request):
    user_id = request.user.id
    cloud_document = Document.objects.filter(user_id=user_id)
    document_form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_manager:upload_document')
        elif Exception:
            return render(request, "file_manager/upload_document.html",
                          context={'form': DocumentForm(), "message": "Form not valid"})

    context = {
        'cloud_document': cloud_document,
        'document_form': document_form,

    }
    return render(request, 'file_manager/upload_document.html', context=context)


def upload_audio(request):
    user_id = request.user.id
    cloud_audio = Audio.objects.filter(user_id=user_id)
    audio_form = AudioForm()
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_manager:upload_audio')
            # audio = form.cleaned_data['audio']
            # result = uploader.upload(audio, resource_type='auto')
            # audio_url = result['secure_url']

            # Збереження аудіо в базі даних або інші дії з ним

    context = {
        'cloud_audio': cloud_audio,
        'audio_form': audio_form,
    }
    return render(request, 'file_manager/upload_audio.html', context=context)


def gallery(request):
    context = {

    }
    return render(request, 'file_manager/gallery.html', context=context)
