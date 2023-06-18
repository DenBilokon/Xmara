import csv
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contacts, File
from datetime import date, datetime, timedelta
from django.db import IntegrityError
from django.contrib import messages


def main(request):
    contacts = Contacts.objects.filter(user=request.user).all().order_by('id') if request.user.is_authenticated else []
    contacts_per_page = 10
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user, 'page': page})


@login_required
def search_contact(request):
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
    contacts_all = Contacts.objects.all()
    current_year = date.today().year
    birthday_list = []
    show = []
    for i in contacts_all:
        if date.today() <= (datetime.strptime(i.birthday, '%Y-%m-%d').date()).replace(
                current_year) < date.today() + timedelta(7):
            birthday_list.append(i)
    return render(request, 'contacts/birthday.html',
                  context={'current_day': current_year, 'birthday_list': birthday_list, 'today': date.today(),
                           'show': show})


@login_required
def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, )
        if form.is_valid():
            contacts = form.save(commit=False)
            contacts.user = request.user
            contacts.save()
            messages.success(request, "Contact was  created successfully !")
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
    contact = Contacts.objects.get(pk=contact_id, user=request.user)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        return redirect(to='contacts:main')
    return render(request, 'contacts/edit.html', context={'form': form, 'contact': contact})


@login_required
def sort(request):
    contacts = Contacts.objects.filter(user=request.user).all().order_by(
        'firstname') if request.user.is_authenticated else []
    contacts_per_page = 10
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user, 'page': page})


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
        try:
            for row in csv_reader:
                model_instance = Contacts()
                model_instance.firstname = row[0].strip()
                model_instance.lastname = row[1].strip()
                model_instance.phone = row[2].strip()
                model_instance.email = row[3].strip()
                model_instance.birthday = datetime.strptime(row[4].strip('\t'), '%Y-%m-%d').date()
                model_instance.save()
        except:
            #messages.warning(request, 'Your format of CSV file unfitisfied !')
            return redirect(to='contacts:main')


@login_required
def file_uploader(request):
    if request.method == 'POST':
        file = request.FILES.get('file', False)
        if not file.name.endswith('.csv'):
            messages.warning(request, 'Invalid file format. Please upload a CSV file.')
            return redirect(to='contacts:main')
            #return HttpResponse('Invalid file format. Please upload a CSV file.')
        else:
            try:
                File.objects.create(file=file, user=request.user)
            except:
                messages.warning(request, 'Your format of CSV file unfitisfied !')
                return redirect(to='contacts:main')
            file_path = f'media/files/{file}'
            with open(file_path, 'rb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            try:
                file.user = request.user
                save_csv_to_model(file_path)
            except:
                messages.warning(request, 'Your format of CSV file unfitisfied !')

            contacts = Contacts.objects.filter(user=request.user).all() if request.user.is_authenticated else []
            contacts_per_page = 10
            paginator = Paginator(contacts, contacts_per_page)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            messages.success(request, "File was uploaded successfully")
            return render(request, 'contacts/index.html', context={'page': page})
    contacts = Contacts.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    contacts_per_page = 10
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'page': page})


# try:
#     with open(file_path, 'rb+') as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)
#     save_csv_to_model(file_path)
#     contacts = Contacts.objects.filter(user=request.user).all() if request.user.is_authenticated else []
#     contacts_per_page = 10
#     paginator = Paginator(contacts, contacts_per_page)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
# except IntegrityError as e:
#     messages.success(request, "Contact with this email already exist")
# return redirect(to='contacts:main')