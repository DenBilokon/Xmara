from datetime import date

from cloudinary.uploader import upload
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.views import currency_parse, weather_parse
from .models import Picture, Document, Video
from .forms import PictureForm, DocumentForm, VideoForm


@login_required
def main_mf(request):
    currency_info = currency_parse()
    weather_info = weather_parse()
    return render(request, 'file_manager/index.html', context={'currency_info': currency_info,
                                                               'date': date.today().strftime('%d.%m.%Y'),
                                                               'weather_info': weather_info})


def upload_picture(request):
    user_id = request.user.id
    cloud_images = Picture.objects.filter(user_id=user_id)
    image_form = dict(backend_form=PictureForm())

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        image_form['posted'] = form.instance
        if form.is_valid():
            form.save()

    currency_info = currency_parse()
    weather_info = weather_parse()
    context = {
        'currency_info': currency_info,
        'date': date.today().strftime('%d.%m.%Y'),
        'weather_info': weather_info,
        'cloud_images': cloud_images,
        'image_form': image_form['backend_form']
    }
    return render(request, 'file_manager/upload_picture.html', context=context)


def upload_video(request):
    user_id = request.user.id
    cloud_video = Video.objects.filter(user_id=user_id)
    video_form = dict(backend_form=VideoForm())
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        video_form['posted'] = form.instance
        if form.is_valid():
            form.save()

    weather_info = weather_parse()
    context = {

        'date': date.today().strftime('%d.%m.%Y'),
        'weather_info': weather_info,
        'cloud_video': cloud_video,
        'video_form': video_form['backend_form']
    }
    return render(request, 'file_manager/upload_video.html', context=context)


def upload_document(request):
    user_id = request.user.id
    cloud_document = Document.objects.filter(user_id=user_id)
    document_form = dict(backend_form=DocumentForm())
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        document_form['posted'] = form.instance
        if form.is_valid():
            document = form.cleaned_data['document']
            result = upload(document, resource_type='raw')
            document_url = result['secure_url']

            document = form.save(commit=False)
            document.document_url = document_url
            document.save()
            print(document_url)
            print(result)

    weather_info = weather_parse()
    context = {
        'date': date.today().strftime('%d.%m.%Y'),
        'weather_info': weather_info,
        'cloud_document': cloud_document,
        'document_form': document_form,

    }
    return render(request, 'file_manager/upload_document.html', context=context)


def upload_audio(request):
    # user_id = request.user.id
    # cloud_video = Video.objects.filter(user_id=user_id)
    # video_form = dict(backend_form=VideoForm())
    # if request.method == 'POST':
    #     form = VideoForm(request.POST, request.FILES)
    #     video_form['posted'] = form.instance
    #     if form.is_valid():
    #         form.save()

    weather_info = weather_parse()
    context = {
        'date': date.today().strftime('%d.%m.%Y'),
        'weather_info': weather_info,
        # 'cloud_video': cloud_video,
        # 'video_form': video_form['backend_form']
    }
    return render(request, 'file_manager/upload_audio.html', context=context)


def gallery(request):

    weather_info = weather_parse()
    context = {
        'date': date.today().strftime('%d.%m.%Y'),
        'weather_info': weather_info,

    }
    return render(request, 'file_manager/gallery.html', context=context)
