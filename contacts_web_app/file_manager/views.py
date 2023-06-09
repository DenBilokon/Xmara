from datetime import date

from django.shortcuts import render
from users.views import currency_parse, weather_parse
from .models import Library


def main_mf(request):
    currency_info = currency_parse()
    weather_info = weather_parse()
    return render(request, 'file_manager/index.html', context={'currency_info': currency_info,
                                                               'date': date.today().strftime('%d.%m.%Y'),
                                                               'weather_info': weather_info})


def images(request):
    cloud_images = Library.objects.all()
    currency_info = currency_parse()
    weather_info = weather_parse()
    return render(request, 'file_manager/images.html', context={'currency_info': currency_info,
                                                               'date': date.today().strftime('%d.%m.%Y'),
                                                               'weather_info': weather_info,
                                                               'cloud_images': cloud_images})
