import csv
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contacts, File
from datetime import date, datetime, timedelta


def main(request):
    """
    The main function is the entry point for the contacts app.
    It renders a list of all contacts in the database, if any exist.
    If no user is logged in, it will render an empty list.
    
    :param request: Get the current user
    :return: A rendered template
    :doc-author: Trelent
    """
    contacts = Contacts.objects.filter(user=request.user).all() if request.user.is_authenticated else []

    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user})


@login_required
def search_contact(request):
    """
    The search_contact function is used to search for a contact in the database.
        The function takes in a request object and returns either the main page or 
        renders the search_contact template with context containing searched, contacts.
    
    
    :param request: Get the request object
    :return: A render of the search_contact
    :doc-author: Trelent
    """
    if request.method == 'POST':
        searched = request.POST['searched']
        if len(searched) > 1:
            contacts = Contacts.objects.filter(firstname__contains=searched,
                                               user=request.user).all() | Contacts.objects.filter(
                lastname__contains=searched, user=request.user).all() | Contacts.objects.filter(
                email__contains=searched, user=request.user).all()
            return render(request, 'contacts/search_contact.html',
                          context={'searched': searched, 'contacts': contacts})
        return redirect(to='contacts:main')
    else:
        return render(request, 'contacts/search_contact.html')


@login_required
def birthday(request):
    """
    The birthday function takes the request and returns a rendered template of all contacts whose birthday is within
    the next 7 days. It also includes the current year, today's date, and an empty list for show.
    
    :param request: Get the request object
    :return: The current_year, birthday_list, today and show
    :doc-author: Trelent
    """
    contacts_all = Contacts.objects.all()
    current_year = date.today().year
    birthday_list = []
    show = []
    for i in contacts_all:
        if date.today() < (datetime.strptime(i.birthday, '%Y-%m-%d').date()).replace(
                current_year) < date.today() + timedelta(7):
            birthday_list.append(i)
    return render(request, 'contacts/birthday.html',
                  context={'current_day': current_year, 'birthday_list': birthday_list, 'today': date.today(),
                           'show': show})


@login_required
def contacts(request):
    """
    The contacts function is a view that allows users to add contacts.
        It takes in the request and returns a rendered template of the contact form.
        If the user submits data, it will be saved to the database.
    
    :param request: Pass the request object to the view
    :return: The html page with the form
    :doc-author: Trelent
    """
    if request.method == 'POST':
        form = ContactForm(request.POST, )
        if form.is_valid():
            contacts = form.save(commit=False)
            contacts.user = request.user
            contacts.save()
            return redirect(to='contacts:main')
        else:
            return render(request, 'contacts/contact.html', {'form': form})
    return render(request, 'contacts/contact.html', {'form': ContactForm()})


@login_required
def delete_contact(request, contact_id):
    """
    The delete_contact function deletes a contact from the database.
        Args:
            request (HttpRequest): The HTTP request sent to the server.
            contact_id (int): The primary key of the Contact object to be deleted.
    
    :param request: Get the current user
    :param contact_id: Identify the contact to be deleted
    :return: A redirect to the main page
    :doc-author: Trelent
    """
    Contacts.objects.get(pk=contact_id, user=request.user).delete()
    return redirect(to='contacts:main')


@login_required
def edit(request, contact_id):
    """
    The edit function is used to edit a contact.
        It takes in the request and contact_id as parameters.
        The function then gets the contact from Contacts model using the primary key of that object, which is also equal to 
        the user who created it. Then we create an instance of ContactForm with either POST data or None if there's no POST data, 
        and pass in our instance variable (contact). If form is valid, save it and redirect back to main page; otherwise render 
        edit template with context containing form and contact variables.
    
    :param request: Get the user information, contact_id is used to find the specific contact and then save it
    :param contact_id: Get the contact object from the database
    :return: The edit
    :doc-author: Trelent
    """
    contact = Contacts.objects.get(pk=contact_id, user=request.user)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        return redirect(to='contacts:main')
    return render(request, 'contacts/edit.html', context={'form': form, 'contact': contact})


@login_required
def sort(request):
    """
    The sort function is used to sort the contacts by first name.
        
    
    :param request: Get the current user
    :return: The firstname of the contacts in alphabetical order
    :doc-author: Trelent
    """
    contacts = Contacts.objects.filter(user=request.user).all().order_by(
        'firstname').values() if request.user.is_authenticated else []
    return render(request, 'contacts/index.html', context={'contacts': contacts})


def save_csv_to_model(file_path):
    """
    The save_csv_to_model function takes a file path as an argument and saves the data in that CSV to the Contacts model.
    The function opens the file, reads it line by line, skips over the header row (firstname, lastname...), and then creates a new instance of Contacts for each row in the CSV.
    It then assigns values from each column to attributes on that instance of Contacts before saving it.
    
    :param file_path: Specify the path to the csv file
    :return: A none type
    :doc-author: Trelent
    """
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            model_instance = Contacts()
            model_instance.firstname = row[0]
            model_instance.lastname = row[1]
            model_instance.phone = row[2]
            model_instance.email = row[3]
            model_instance.birthday = datetime.strptime(row[4].strip(), '%Y-%m-%d').date()
            model_instance.save()


@login_required
def file_uploader(request):
    """
    The file_uploader function is responsible for handling the file upload process.
    It first checks if the request method is POST, which means that a file has been uploaded.
    If so, it creates an instance of File with the uploaded file and user who uploaded it.
    Then, it saves the CSV to a model using save_csv_to_model function (see below). 
    Afterwards, it converts CSV to JSON and saves this JSON in media/files folder.
    
    :param request: Get the file from the form
    :return: A redirect to the main page
    :doc-author: Trelent
    """
    if request.method == 'POST':
        file = request.FILES['file']
        File.objects.create(file=file, user=request.user)
        file_path = f'media/files/{file}'
        with open(file_path, 'rb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        save_csv_to_model(file_path)
        data = []
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append({k.strip(): v.strip() for k, v in row.items()})
        with open(f'media/files/{file}.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        return redirect(to='contacts:main')
    return render(request, 'contacts/index.html',
                  context={})


@login_required
def show_files(request):
    """
    The show_files function is a view that displays all of the files uploaded by the user.
        It takes in a request object and returns an HTML page with all of the files uploaded by
        that user.
    
    :param request: Get the current user
    :return: The files
    :doc-author: Trelent
    """
    files = File.objects.filter(user=request.user).all()
    return render(request, 'contacts/files.html', context={'files': files, "media": settings.MEDIA_URL})
