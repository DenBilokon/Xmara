from datetime import date

from django.shortcuts import render
from users.views import currency_parse


def main_mf(request):
    currency_info = currency_parse()
    return render(request, 'file_manager/index.html', context={'currency_info': currency_info,
                                                               'date': date.today().strftime('%d.%m.%Y')})


