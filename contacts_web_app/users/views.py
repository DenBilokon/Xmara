import openai

from datetime import date

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from cloudinary.exceptions import Error as CloudinaryError

from .forms import RegisterForm, AvatarForm
from .models import Avatar

from contacts_web_app.settings import OPENAI_KEY

date_today = date.today().strftime('%d.%m.%Y')


def main(request):
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    return render(request, 'users/index.html', context={'avatar': avatar})


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/signup.html'

    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch function is a method that gets called when the view is requested.
        It checks if the user is authenticated, and if so redirects them to the home page.
        If not, it calls super().dispatch() which will call get(), post(), etc.
        
        :param self: Refer to the current instance of the class
        :param request: Get the request object, which is used to check if the user is authenticated
        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A redirect to the home page if user is authenticated, otherwise it returns a super()
        :doc-author: Xmara
        """
        if self.request.user.is_authenticated:
            return redirect(to='quotes:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        The get function renders the form to the user.
            
        
        :param self: Access the attributes and methods of the class in python
        :param request: Get the request object
        :return: A render of the template_name with the form_class
        :doc-author: Xmara
        """
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        """
        The post function is used to create a new user.
            The form_class variable is set to the UserCreationForm class, which allows us to create a new user.
            The form variable is set equal to the post request and cleaned data from the UserCreationForm class.
            If the form has been filled out correctly, then it will save that information into our database and redirect you back 
        to login page with a success message.
        
        :param self: Represent the instance of the object itself
        :param request: Pass the request object to the view
        :return: The render function which renders the template
        :doc-author: Xmara
        """
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
    """
    The user_data function renders the user.html template, which displays a list of all users in the database.
    
    :param request: Pass the request object to the view
    :return: The user
    :doc-author: Xmara
    """
    return render(request, "users/user.html", context={})


def question_to_ai(request):
    """
    The question_to_ai function is used to get a question from the user and send it to OpenAI.
        The function then gets an answer from OpenAI, which is returned as a response_html variable.
        This variable is passed into the context of the index page, where it will be displayed in
        place of any previous answer.

    :param request: Get the user's request
    :return: The answer of the OpenAI to the user's question
    :doc-author: Xmara
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
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

    return render(request, 'users/index.html', context={'answer_for_user': response_html, 'avatar': avatar})


@login_required
def upload_avatar(request):
    """
    The upload_avatar function allows a user to upload an avatar image.
        The function first checks if the request method is POST, and if so, it instantiates the AvatarForm with
        the request data and files. If form is valid, it saves the uploaded file as an avatar for that user.
        If there was already an existing avatar for that user, then delete it before saving new one.

    :param request: Get the current user
    :return: A render function that renders the user_upload_avatar
    :doc-author: Xmara
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    form = AvatarForm()  # Instantiate the form

    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                previous_avatar = Avatar.objects.filter(user=request.user).first()
                avatar = form.save(commit=False)
                avatar.user = request.user

                # Validate if the uploaded file is an image
                uploaded_file = form.cleaned_data['image']
                if not uploaded_file.content_type.startswith('image'):
                    raise ValidationError("Invalid file format. Please upload an image.")

                avatar.save()
                if previous_avatar:
                    previous_avatar.delete()

                return redirect('users:profile')
            except (CloudinaryError, ValidationError) as e:
                messages.warning(request, "Invalid file format.")

    return render(request, 'users/user_upload_avatar.html', {'form': form, 'avatar': avatar})


@login_required
def profile(request):
    """
    The profile function is used to render the profile page of a user.
    It takes in a request object and returns an HttpResponse object with the rendered template.
    The function first gets the current user from the request, then it gets their id, and finally it uses that id to
    get their avatar from Avatar model.

    :param request: Get the current user
    :return: A dictionary with the user and avatar
    :doc-author: Xmara
    """
    user = request.user
    user_id = request.user.id
    avatar = Avatar.objects.filter(user_id=user_id).first()
    return render(request, 'users/profile.html', context={'user': user, 'avatar': avatar})
