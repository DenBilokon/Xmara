from datetime import date

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.views import currency_parse, weather_parse
from .models import Library
from .forms import LibraryForm


@login_required
def main_mf(request):
    currency_info = currency_parse()
    weather_info = weather_parse()
    return render(request, 'file_manager/index.html', context={'currency_info': currency_info,
                                                               'date': date.today().strftime('%d.%m.%Y'),
                                                               'weather_info': weather_info})


def images(request):
    user_id = request.user.id
    cloud_images = Library.objects.filter(user_id=user_id)
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            library = form.save(commit=False)
            library.user = request.user
            library.save()
            return redirect('library_detail', library_id=library.id)

    form = LibraryForm()
    currency_info = currency_parse()
    weather_info = weather_parse()
    return render(request, 'file_manager/images.html', context={'currency_info': currency_info,
                                                                'date': date.today().strftime('%d.%m.%Y'),
                                                                'weather_info': weather_info,
                                                                'cloud_images': cloud_images,
                                                                'form': form})


def create_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            library = form.save(commit=False)
            library.user = request.user
            library.save()
            return redirect('library_detail', library_id=library.id)
    else:
        form = LibraryForm()

    return render(request, 'create_library.html', {'form': form})