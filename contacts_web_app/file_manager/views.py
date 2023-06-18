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
    """
    The main_mf function is the main view for the file manager.
    It renders a template with an avatar object, which is used to display
    the user's profile picture in the top right corner of the page.
    
    :param request: Get the user's avatar from the database
    :return: A render with the context of avatar
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return render(request, 'file_manager/index.html', context={'avatar': avatar})


@login_required
def upload_picture(request):
    """
    The upload_picture function is responsible for uploading a picture to the cloudinary server.
    It also displays all of the pictures that have been uploaded by the user.
    
    :param request: Get the request object
    :return: The render function
    """
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
    """
    The download_image function takes a request and an image_url as arguments.
    It then makes a GET request to the image_url, gets the content-type from the response headers,
    and saves it in a variable called content_type. It also splits up the URL into its component parts using split(),
    and saves only the last part of that list (the filename) in another variable called filename. 
    Then it creates an HttpResponse object with response's content and our previously saved content type, 
    sets Content-Disposition to attachment; filename=&quot;{filename}&quot;, and returns this new HttpResponse object.
    
    :param request: Get the request object
    :param image_url: Pass the image url to the function
    :return: An image file with the specified url
    """
    response = requests.get(image_url)
    content_type = response.headers.get('content-type')
    filename = image_url.split('/')[-1]  # Отримати назву файлу з URL
    response = HttpResponse(response.content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@login_required
def delete_picture(request, picture_id):
    """
    The delete_picture function takes a request and picture_id as arguments.
    It gets the picture with the given id, which is owned by the user making
    the request, and deletes it. It then displays a success message to let them know
    that their picture was deleted successfully.
    
    :param request: Get the current user
    :param picture_id: Get the picture that we want to delete
    :return: The redirect function which returns a httpresponseredirect object
    """
    picture = Picture.objects.get(id=picture_id, user=request.user)
    picture.delete()
    messages.success(request, "Picture deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_picture(request):
    """
    The search_picture function is used to search for a picture in the database.
        The function takes a request as an argument and returns the result of searching
        for pictures by title.
    
    :param request: Get the request object
    :return: The search_picture
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    query = request.GET.get("q")
    if query:
        files = Picture.objects.filter(Q(title__icontains=query))
        files_search = pagination(request, files)
        context = {
            "query": query,
            "cloud_images": files_search,
            'avatar': avatar
        }
        return render(request, "file_manager/search_picture.html", context=context)
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_video(request):
    """
    The upload_video function is responsible for uploading a video to the cloudinary server.
        It also displays all videos uploaded by the user on the same page.
    
    :param request: Get the request object
    :return: A render of the upload_video
    """
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
    """
    The delete_video function deletes a video from the database.
        Args:
            request (HttpRequest): The request object sent by the user.
            video_id (int): The id of the video to be deleted.
    
    :param request: Get the current user
    :param video_id: Identify the video that is to be deleted
    :return: The http_referer
    """
    video = Video.objects.get(id=video_id, user=request.user)
    video.delete()
    messages.success(request, "Video deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_video(request):
    """
    The search_video function is used to search for videos in the database.
        The function takes a request object as an argument and returns a rendered template with the results of the query.
        If there are no results, it redirects back to where it came from.
    
    :param request: Get the request object from the view
    :return: The following error:
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    query = request.GET.get("q")
    if query:
        files = Video.objects.filter(Q(title__icontains=query))
        files_search = pagination(request, files)
        context = {
            "query": query,
            "cloud_video": files_search,
            'avatar': avatar
        }
        return render(request, "file_manager/search_video.html", context=context)
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_document(request):
    """
    The upload_document function is responsible for uploading documents to the cloud.
        It also displays all uploaded documents on the page.
    
    :param request: Get the request object
    :return: A redirect to the same page
    """
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
    """
    The delete_document function deletes a document from the database.
        Args:
            request (HttpRequest): The request object sent by the user.
            document_id (int): The id of the document to be deleted.
    
    :param request: Get the current user
    :param document_id: Get the document that is to be deleted
    :return: A redirect to the previous page
    """
    document = Document.objects.get(id=document_id, user=request.user)
    document.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_document(request):
    """
    The search_document function is used to search for documents in the database.
        The function takes a request as an argument and returns a rendered template with the results of the query.
        If there is no query, then it redirects to another page.
    
    :param request: Get the request object
    :return: The search_document
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    query = request.GET.get("q")
    if query:
        files = Document.objects.filter(Q(title__icontains=query))
        files_search = pagination(request, files)
        context = {
            "query": query,
            "cloud_document": files_search,
            'avatar': avatar
        }
        return render(request, "file_manager/search_document.html", context=context)
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


@login_required
def upload_audio(request):
    """
    The upload_audio function is responsible for uploading audio files to the cloudinary server.
    It also displays all of the uploaded audio files on a page.
    
    :param request: Get the request object
    :return: The file_manager/upload_audio
    """
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
    """
    The delete_audio function deletes an audio file from the database.
        It takes a request and an audio_id as parameters, then uses the Audio model to get the audio object with that id.
        The function then deletes that object and redirects back to where it came from.
    
    :param request: Get the user from the request object
    :param audio_id: Get the audio object from the database
    :return: A redirect to the previous page
    """
    audio = Audio.objects.get(id=audio_id, user=request.user)
    audio.delete()
    messages.success(request, "Audio deleted successfully.")
    return redirect(request.META['HTTP_REFERER'])


def search_audio(request):
    """
    The search_audio function is used to search for audio files in the database.
        The function takes a request as an argument and returns a rendered template with the results of the search.
    
    :param request: Get the request object from the view
    :return: The result of the search for audio files
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    query = request.GET.get("q")
    if query:
        files = Audio.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        files_search = pagination(request, files)
        context = {
            "query": query,
            "cloud_audio": files_search,
            'avatar': avatar
        }
        return render(request, "file_manager/search_audio.html", context=context)
    messages.success(request, "Enter your request.")
    return redirect(request.META['HTTP_REFERER'])


def pagination(request, files):
    """
    The pagination function takes in a request and a list of files.
    It then creates a paginator object with the number of items per page set to 20,
    and the list of files as its argument. It then gets the current page number from 
    the request, and returns an object containing that page's information.
    
    :param request: Get the page number from the url
    :param files: Pass in the queryset of files to be paginated
    :return: A page object
    """
    per_page = 20
    paginator = Paginator(list(files), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
