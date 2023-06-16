import requests

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Picture, Document, Video, Audio
from .forms import PictureForm, DocumentForm, VideoForm, AudioForm


@login_required
def main_mf(request):
    return render(request, 'file_manager/index.html', context={})


@login_required
def upload_picture(request):
    user_id = request.user.id
    cloud_images = Picture.objects.filter(user_id=user_id)
    per_page = 20
    paginator = Paginator(list(cloud_images), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    image_form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)

        if form.is_valid():
            pic = form.save(commit=False)
            pic.user = request.user
            pic.save()
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'cloud_images': page_obj,
        'image_form': image_form
    }
    return render(request, 'file_manager/upload_picture.html', context=context)


@login_required
def download_image(request, image_url):
    response = requests.get(image_url)
    content_type = response.headers.get('content-type')
    filename = image_url.split('/')[-1]  # Отримати назву файлу з URL
    print(filename)

    # Налаштувати заголовки відповіді для завантаження файлу
    response = HttpResponse(response.content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@login_required
def delete_picture(request, picture_id):
    picture = Picture.objects.get(id=picture_id, user=request.user)
    picture.delete()
    messages.success(request, "Picture deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_video(request):
    user_id = request.user.id
    cloud_video = Video.objects.filter(user_id=user_id)
    video_form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        # video_form['posted'] = form.instance
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect(request.META['HTTP_REFERER'])
        elif Exception:
            return render(request, "file_manager/upload_video.html",
                          context={'form': VideoForm(), "message": "Form not valid"})

    context = {
        'cloud_video': cloud_video,
        'video_form': video_form,
    }
    return render(request, 'file_manager/upload_video.html', context=context)


@login_required
def upload_document(request):
    user_id = request.user.id
    cloud_document = Document.objects.filter(user_id=user_id)
    document_form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.user = request.user
            doc.save()
            return redirect('file_manager:upload_document')
        elif Exception:
            return render(request, "file_manager/upload_document.html",
                          context={'form': DocumentForm(), "message": "Form not valid"})

    context = {
        'cloud_document': cloud_document,
        'document_form': document_form,

    }
    return render(request, 'file_manager/upload_document.html', context=context)


@login_required
def upload_audio(request):
    user_id = request.user.id
    cloud_audio = Audio.objects.filter(user_id=user_id)
    audio_form = AudioForm()
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            aud = form.save(commit=False)
            aud.user = request.user
            aud.save()
            return redirect(request.META['HTTP_REFERER'])
            # audio = form.cleaned_data['audio']
            # result = uploader.upload(audio, resource_type='auto')
            # audio_url = result['secure_url']

            # Збереження аудіо в базі даних або інші дії з ним

    context = {
        'cloud_audio': cloud_audio,
        'audio_form': audio_form,
    }
    return render(request, 'file_manager/upload_audio.html', context=context)


@login_required
def gallery(request):
    context = {

    }
    return render(request, 'file_manager/gallery.html', context=context)
