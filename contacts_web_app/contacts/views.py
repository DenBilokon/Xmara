import csv
import os
from io import TextIOWrapper

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contacts, File
from datetime import date, datetime, timedelta
from django.contrib import messages

from users.models import Avatar


def main(request):
    """
    The main function is the main page of the contacts app.
    It displays all contacts for a user, if they are logged in.
    If not, it displays an error message.

    :param request: Get the current user
    :return: A list of contacts
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    contacts = Contacts.objects.filter(user=request.user).all().order_by('id') if request.user.is_authenticated else []
    contacts_per_page = 15
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user, 'page': page, 'avatar': avatar})


@login_required
def search_contact(request):
    """
    The search_contact function is used to search for a contact in the database.
    It takes a request as an argument and returns the searched contacts if they exist.

    :param request: Get the request object from the browser
    :return: The search_contact
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    if request.method == 'POST':
        searched = request.POST['searched']
        if len(searched) > 1:
            contacts = Contacts.objects.filter(firstname__contains=searched,
                                               user=request.user).all() | Contacts.objects.filter(
                lastname__contains=searched, user=request.user).all() | Contacts.objects.filter(
                email__contains=searched, user=request.user).all()
            return render(request, 'contacts/search_contact.html',
                          context={'searched': searched, 'contacts': contacts, 'avatar': avatar})
        return redirect(to='contacts:main')
    else:
        return render(request, 'contacts/search_contact.html')


@login_required
def birthday(request):
    """
    The birthday function is used to display the contacts that have a birthday in the next 7 days.
    It takes request as an argument and returns a render of the birthday template with context containing:
    current_day, which is today's year;
    birthday_list, which contains all contacts that have birthdays in the next 7 days;
    today, which is today's date;
    show, an empty list for use later on when we add search functionality to this page (see below); and avatar.

    :param request: Get the current user
    :return: The list of contacts whose birthday is in the next 7 days
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    contacts_all = Contacts.objects.all()
    current_year = date.today().year
    birthday_list = []
    show = []
    for i in contacts_all:
        if date.today() <= (datetime.strptime(i.birthday.strip('\t'), '%Y-%m-%d').date().replace(
                year=current_year)) < date.today() + timedelta(7):
            birthday_list.append(i)
    return render(request, 'contacts/birthday.html',
                  context={'current_day': current_year, 'birthday_list': birthday_list, 'today': date.today(),
                           'show': show, 'avatar': avatar})


@login_required
def contacts(request):
    """
    The contacts function is used to create a new contact.
        It takes the request as an argument and returns a rendered template with the form.
        If the request method is POST, it will validate and save the data from that form.

    :param request: Get the request object
    :return: The contact page with the form and avatar
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    if request.method == 'POST':
        form = ContactForm(request.POST, )
        if form.is_valid():
            contacts = form.save(commit=False)
            contacts.user = request.user
            contacts.save()
            messages.success(request, "Contact was  created successfully !")
            return redirect(request.META['HTTP_REFERER'])
        else:
            return render(request, 'contacts/contact.html', {'form': form, 'avatar': avatar})
    return render(request, 'contacts/contact.html', {'form': ContactForm(), 'avatar': avatar})


@login_required
def delete_contact(request, contact_id):
    """
    The delete_contact function is called when the user clicks on the delete button
    on a contact's page. It deletes that contact from the database and redirects to
    the main contacts page.

    :param request: Get the user from the request object
    :param contact_id: Find the contact to delete
    :return: A redirect to the main page
    :doc-author: Trelent
    """
    Contacts.objects.get(pk=contact_id, user=request.user).delete()
    return redirect(request.META['HTTP_REFERER'])


@login_required
def edit(request, contact_id):
    """
    The edit function is used to edit a contact.
        It takes the request and contact_id as parameters,
        then it gets the avatar of the user,
        then it gets the contact with that id and for that user,
        then it creates a form using ContactForm class with instance=contact (to fill in fields),
            if this form is valid: save changes to database and redirect to main page.

    :param request: Get the current request, which is used to get the user
    :param contact_id: Get the contact from the database
    :return: The edit
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    contact = Contacts.objects.get(pk=contact_id, user=request.user)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        messages.success(request, "Contact was updated successfully !")
        return redirect(to='contacts:main')
    return render(request, 'contacts/edit.html', context={'form': form, 'contact': contact,
                                                          'avatar': avatar})


@login_required
def sort(request):
    """
    The sort function is used to sort the contacts by first name.
    It takes in a request and returns a render of the index page with the sorted contacts.

    :param request: Get the request object
    :return: The contacts sorted by firstname
    :doc-author: Trelent
    """
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    contacts = Contacts.objects.filter(user=request.user).all().order_by(
        'firstname') if request.user.is_authenticated else []
    contacts_per_page = 15
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user, 'page': page,
                           'avatar': avatar})


current_dir = os.path.dirname(os.path.abspath(__file__))


def save_csv_to_model(file_path):
    """
    The save_csv_to_model function takes a file path as an argument and saves the data in that CSV to the Contacts model.
    It does this by opening the file, reading it with csv.reader, skipping over the header row, and then iterating through each row of data in order to create a new instance of Contacts for each row.

    :param file_path: Specify the path to the file that we want to import
    :return: A list of the saved instances
    :doc-author: Trelent
    """
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            model_instance = Contacts()
            model_instance.firstname = row[0].strip()
            model_instance.lastname = row[1].strip()
            model_instance.phone = row[2].strip()
            model_instance.email = row[3].strip()
            model_instance.birthday = datetime.strptime(row[4].strip('\t'), '%Y-%m-%d').date()
            model_instance.save()


@login_required
def file_uploader(request):
    """
    The file_uploader function is responsible for uploading a CSV file to the server.
    It also saves the uploaded file in the database and then calls save_csv_to_model function, which saves all contacts from
    the CSV file into Contacts model.

    :param request: Get the request object
    :return: A render function that renders the index
    :doc-author: Trelent
    """

    if request.method == 'POST':
        try:
            csv_file = request.FILES.get('file')
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'Invalid file format. Please upload a CSV file.')
                return redirect(to='contacts:main')
            csv_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.reader(csv_file_wrapper)
            next(reader)
            print(reader)

            for row in reader:
                try:
                    contacts = Contacts(
                        firstname=row[0],
                        lastname=row[1],
                        phone=row[2],
                        email=row[3],
                        birthday=row[4],
                        user=request.user,
                    )
                    contacts.save()
                except:
                    messages.warning(request, 'Wrong data in your CSV')
                    return redirect(to='contacts:main')

            messages.success(request, "File was uploaded successfully")
            return redirect(to='contacts:main')
        except AttributeError:
            messages.warning(request, 'You forgot to choose a file. Please make sure you chose CSV file and upload it.')
            return redirect(to='contacts:main')
    avatar = Avatar.objects.filter(user_id=request.user.id).first()
    contacts = Contacts.objects.filter(user=request.user).all().order_by('id') if request.user.is_authenticated else []
    contacts_per_page = 15
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user, 'page': page, 'avatar': avatar})
