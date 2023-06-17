import csv
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
    if request.method == 'POST':
        file = request.FILES['file']
        File.objects.create(file=file, user=request.user)
        file_path = f'media/files/{file}'
        try:
            with open(file_path, 'rb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            save_csv_to_model(file_path)
            contacts = Contacts.objects.filter(user=request.user).all() if request.user.is_authenticated else []
            contacts_per_page = 10
            paginator = Paginator(contacts, contacts_per_page)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
        except IntegrityError as e:
            messages.success(request, "Contact with this email already exist")
        return redirect(to='contacts:main')
        data = []
        # with open(file_path, 'r', encoding='utf-8') as csv_file:
        #     csv_reader = csv.DictReader(csv_file)
        #     for row in csv_reader:
        #         data.append({k.strip(): v.strip() for k, v in row.items()})
        # with open(f'media/files/{file}.json', 'w') as outfile:
        #     json.dump(data, outfile, indent=4)

    return render(request, 'contacts/index.html',
                  context={'page': page})
