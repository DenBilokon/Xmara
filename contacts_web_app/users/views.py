import requests
import json

from datetime import date

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import RegisterForm

from contacts_web_app.settings import WEATHER_API


def main(request):
    currency_info = currency_parse()
    weather_info = weather_parse()
    return render(request, 'users/index.html', context={'currency_info': currency_info,
                                                        'date': date.today().strftime('%d.%m.%Y'),
                                                        'weather_info': weather_info})


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(to='quotes:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Hello {username}! Your account has been created.")
            return redirect(to="users:login")
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'


def user_data(request):
    return render(request, "users/user.html", context={})


def currency_parse():
    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date.today().strftime('%d.%m.%Y')}"
    response = requests.get(url)
    currency_data = json.loads(response.text).get('exchangeRate')
    currency_dict = {"currency_USD": currency_data[23],
                     "currency_EUR": currency_data[8],
                     "currency_GBR": currency_data[9],
                     "currency_PLN": currency_data[17]}
    return currency_dict


def weather_parse():
    weather_data = {}
    cities = ['London', 'Prague', 'Berlin', 'Paris', 'Stockholm', 'Warsaw']
    for city in cities:
        url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={city}'
        response = requests.get(url)
        city_data = json.loads(response.text).get('current')
        city_dict = {'city': city,
                     'temp_c': city_data.get('temp_c'),
                     'wind_kph': city_data.get('wind_kph'),
                     'icon': city_data.get('condition').get('icon'),
                     'text': city_data.get('condition').get('text')}
        weather_data[city] = city_dict
    return weather_data

# {'London': {'city': 'London', 'temp_c': 24.0, 'wind_kph': 31.0, 'icon': '//cdn.weatherapi.com/weather/64x64/day/389.png', 'text': 'Moderate or heavy rain with thunder'}, 'Prague': {'city': 'Prague', 'temp_c': 24.0, 'wind_kph': 31.0, 'icon': '//cdn.weatherapi.com/weather/64x64/day/389.png', 'text': 'Moderate or heavy rain with thunder'}, 'Berlin': {'city': 'Berlin', 'temp_c': 24.0, 'wind_kph': 31.0, 'icon': '//cdn.weatherapi.com/weather/64x64/day/389.png', 'text': 'Moderate or heavy rain with thunder'}, 'Paris': {'city': 'Paris', 'temp_c': 24.0, 'wind_kph': 31.0, 'icon': '//cdn.weatherapi.com/weather/64x64/day/389.png', 'text': 'Moderate or heavy rain with thunder'}, 'Stockholm': {'city': 'Stockholm', 'temp_c': 24.0, 'wind_kph': 31.0, 'icon': '//cdn.weatherapi.com/weather/64x64/day/389.png', 'text': 'Moderate or heavy rain with thunder'}, 'Warsaw': {'city': 'Warsaw', 'temp_c': 24.0, 'wind_kph': 31.0, 'icon': '//cdn.weatherapi.com/weather/64x64/day/389.png', 'text': 'Moderate or heavy rain with thunder'}}
