from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone

from users.models import Avatar

from .models import UserFileSummary
from file_manager.models import Audio, Picture, Document, Video, Archive
from contacts.models import Contacts
from notes.models import Note


def format_duration(duration):
    days = duration.days
    hours = duration.seconds // 3600
    return f"{days} days, {hours} hours"


def home(request):
    sort_by = request.GET.get('sort_by', 'username')

    if sort_by.startswith('-'):
        field = sort_by[1:]
        reverse_sort_by = field
        if field == 'inactive':
            users = User.objects.all().order_by('-last_login')
        else:
            users = User.objects.all().order_by(f'-{field}')
    else:
        field = sort_by
        reverse_sort_by = f'-{field}'
        if field == 'inactive':
            users = User.objects.all().order_by('last_login')
        else:
            users = User.objects.all().order_by(field)

    current_time = timezone.now()
    for user in users:
        time_since_last_login = current_time - user.last_login
        user.time_since_last_login = format_duration(time_since_last_login)

    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    context = {
        'avatar': avatar,
        'users': users,
        'current_sort': sort_by,
        'reverse_sort_by': reverse_sort_by,
    }
    return render(request, "adminconsole/users.html", context=context)


def user_data(request):
    sort_by = request.GET.get('sort_by', 'username')

    if sort_by.startswith('-'):
        field = sort_by[1:]
        reverse_sort_by = ''
        users = User.objects.all().order_by(field)
    else:
        field = sort_by
        reverse_sort_by = f'-{field}'
        users = User.objects.all().order_by(f'-{field}')

    for user in users:
        audio_count = Audio.objects.filter(user=user).count()
        pictures_count = Picture.objects.filter(user=user).count()
        videos_count = Video.objects.filter(user=user).count()
        documents_count = Document.objects.filter(user=user).count()
        archives_count = Archive.objects.filter(user=user).count()

        contacts_count = Contacts.objects.filter(user=user).count()
        notes_count = Note.objects.filter(user=user).count()
        summary_files_count = audio_count + pictures_count + videos_count + documents_count + archives_count

        user.file_summary = {
            'audio_count': audio_count,
            'pictures_count': pictures_count,
            'videos_count': videos_count,
            'documents_count': documents_count,
            'archives_count': archives_count,
            'summary_files': summary_files_count,
            'contacts_count': contacts_count,
            'notes_count': notes_count,
        }

    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    context = {
        'avatar': avatar,
        'users': users,
        'current_sort': sort_by,
        'reverse_sort_by': reverse_sort_by,
    }
    return render(request, "adminconsole/user_data.html", context=context)

