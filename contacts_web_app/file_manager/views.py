import requests

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cloudinary.exceptions import Error as CloudinaryError

from .models import Picture, Document, Video, Audio
from .forms import PictureForm, DocumentForm, VideoForm, AudioForm

from users.models import Avatar


@login_required
def main_mf(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return render(request, 'file_manager/index.html', context={'avatar': avatar})


@login_required
def upload_picture(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    user_id = request.user.id
    cloud_images = Picture.objects.filter(user_id=user_id)
    page_obj = pagination(request, cloud_images)
    image_form = PictureForm()

    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                pic = form.save(commit=False)
                pic.user = request.user
                pic.save()
                return redirect(request.META['HTTP_REFERER'])
        except CloudinaryError:
            messages.warning(request, "Form not valid.")
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'cloud_images': page_obj,
        'image_form': image_form,
        'avatar': avatar
    }
    return render(request, 'file_manager/upload_picture.html', context=context)


@login_required
def download_image(request, image_url):
    response = requests.get(image_url)
    content_type = response.headers.get('content-type')
    filename = image_url.split('/')[-1]  # Отримати назву файлу з URL

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


def search_picture(request):
    query = request.GET.get("q")
    if query:
        files = Picture.objects.filter(Q(title__icontains=query))
        files_search = pagination(request, files)
        return render(request, "file_manager/search_picture.html", context={"cloud_images": files_search, "query": query})
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


def pagination(request, files):
    per_page = 20
    paginator = Paginator(list(files), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


@login_required
def upload_video(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    user_id = request.user.id
    cloud_video = Video.objects.filter(user_id=user_id)
    page_obj = pagination(request, cloud_video)
    video_form = VideoForm()
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                video = form.save(commit=False)
                video.user = request.user
                video.save()
                return redirect(request.META['HTTP_REFERER'])
            except CloudinaryError:
                messages.warning(request, "Form not valid.")
                return redirect(request.META['HTTP_REFERER'])

    context = {
        'cloud_video': page_obj,
        'video_form': video_form,
        'avatar': avatar
    }
    return render(request, 'file_manager/upload_video.html', context=context)


@login_required
def delete_video(request, video_id):
    video = Video.objects.get(id=video_id, user=request.user)
    video.delete()
    messages.success(request, "Video deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_video(request):
    query = request.GET.get("q")
    if query:
        files = Video.objects.filter(Q(title__icontains=query))
        files_search = pagination(request, files)
        return render(request, "file_manager/search_video.html", context={"cloud_video": files_search, "query": query})
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_document(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    user_id = request.user.id
    cloud_document = Document.objects.filter(user_id=user_id)
    page_obj = pagination(request, cloud_document)
    document_form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                doc = form.save(commit=False)
                doc.user = request.user
                doc.save()
                return redirect(request.META['HTTP_REFERER'])
        except CloudinaryError:
            messages.warning(request, "Form not valid.")
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'cloud_document': page_obj,
        'document_form': document_form,
        'avatar': avatar

    }
    return render(request, 'file_manager/upload_document.html', context=context)


@login_required
def delete_document(request, document_id):
    document = Document.objects.get(id=document_id, user=request.user)
    document.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_document(request):
    query = request.GET.get("q")
    if query:
        files = Document.objects.filter(Q(title__icontains=query))
        files_search = pagination(request, files)
        return render(request, "file_manager/search_document.html", context={"cloud_document": files_search, "query": query})
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_audio(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    user_id = request.user.id
    cloud_audio = Audio.objects.filter(user_id=user_id)
    page_obj = pagination(request, cloud_audio)
    audio_form = AudioForm()
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                aud = form.save(commit=False)
                aud.user = request.user
                aud.save()
                return redirect(request.META['HTTP_REFERER'])
        except CloudinaryError:
            messages.warning(request, "Form not valid.")
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'cloud_audio': page_obj,
        'audio_form': audio_form,
        'avatar': avatar
    }
    return render(request, 'file_manager/upload_audio.html', context=context)


@login_required
def delete_audio(request, audio_id):
    audio = Audio.objects.get(id=audio_id, user=request.user)
    audio.delete()
    messages.success(request, "Audio deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_audio(request):
    query = request.GET.get("q")
    if query:
        files = Audio.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        files_search = pagination(request, files)
        return render(request, "file_manager/search_audio.html", context={"cloud_audio": files_search, "query": query})
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def gallery(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    context = {
        'avatar': avatar
    }
    return render(request, 'file_manager/gallery.html', context=context)
