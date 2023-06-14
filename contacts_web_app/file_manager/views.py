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
    image_form = dict(backend_form=LibraryForm())

    if request.method == 'POST':
        form = LibraryForm(request.POST, request.FILES)
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
    return render(request, 'file_manager/images.html', context=context)