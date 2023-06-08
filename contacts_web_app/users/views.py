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


def main(request):
    currency_info = currency_parse()
    return render(request, 'users/index.html', context={'currency_info': currency_info,
                                                        'date': '08.06.2023'})


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


def currency(request):
    currency_info = currency_parse()
    return render(request, "users/base.html", context={'currency_info': currency_info,
                                                       'date': '08.06.2023'})
