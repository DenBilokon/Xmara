import requests
import json
import openai

from datetime import date

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


from .forms import RegisterForm

from contacts_web_app.settings import OPENAI_KEY

date_today = date.today().strftime('%d.%m.%Y')


def main(request):
    return render(request, 'users/index.html')


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


# def weather_parse():
#     weather_data = {}
#     cities = ['London', 'Prague', 'Berlin', 'Paris', 'Stockholm', 'Warsaw']
#     for city in cities:
#         url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={city}'
#         response = requests.get(url)
#         city_data = json.loads(response.text).get('current')
#         city_dict = {'city': city,
#                      'temp_c': city_data.get('temp_c'),
#                      'wind_kph': city_data.get('wind_kph'),
#                      'icon': city_data.get('condition').get('icon'),
#                      'text': city_data.get('condition').get('text')}
#         weather_data[city] = city_dict
#     return weather_data


def question_to_ai(request):

    openai.api_key = OPENAI_KEY

    question = request.POST.get('question')
    prompt = f'You are website helper. Also, you should know everything about this website from documentation, ' \
             f'answer clearly and a little defiantly, but without exaggeration and no more than 300 symbols ' \
             f'Only truth. Use emoticons to decorate the dialogue. So, the question is - {question}'

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=50,
        temperature=0.7,
        n=1,
        stop=None,
        echo=True
    )

    if 'choices' in response and len(response.choices) > 0:
        answer = response.choices[0].text.strip()
        response_html = f'Your helper-AI: {answer.replace(prompt, "")}'
    else:
        response_html = None

    return render(request, 'users/index.html', context={'answer_for_user': response_html})

