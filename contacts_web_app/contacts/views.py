import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contacts, File
from datetime import date, datetime, timedelta
from django.contrib import messages


def main(request):
    """
    The main function is the main view of the contacts app.
    It displays a list of all contacts for a given user, and allows them to be edited or deleted.
    
    :param request: Get the request object that is sent to the server
    :return: A render function
    """
    contacts = Contacts.objects.filter(user=request.user).all().order_by('id') if request.user.is_authenticated else []
    contacts_per_page = 10
    paginator = Paginator(contacts, contacts_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'contacts/index.html',
                  context={'contacts': contacts, 'user': request.user, 'page': page})


@login_required
def search_contact(request):
    """
    The search_contact function is used to search for a contact in the database.
        The function takes in a request object and returns either the main page or 
        renders the search_contact template with context containing searched, contacts.
    
    :param request: Get the request from the user
    :return: The search_contact
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
    the next 7 days.
    
    :param request: Get the request object
    :return: A list of contacts whose birthday is within 7 days from today
    """
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
    """
    The contacts function is used to create a new contact.
        It takes the request as an argument and returns a rendered template with the form.
        If the method is POST, it will save the data from that form into our database.
    
    :param request: Pass the request object to the function
    :return: A response object
    """
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
    :param contact_id: Identify which contact to delete
    :return: A redirect to the main page
    """
    Contacts.objects.get(pk=contact_id, user=request.user).delete()
    return redirect(to='contacts:main')


@login_required
def edit(request, contact_id):
    """
    The edit function is used to edit a contact.
        It takes the request and contact_id as parameters.
        The function gets the user's contacts from the database, then it creates an instance of ContactForm with that data, 
        and if it is valid, saves it in the database and redirects to main page with a success message. Otherwise renders edit page.
    
    :param request: Get the user information from the request object
    :param contact_id: Get the contact object from the database
    :return: A redirect to the main page
    """
    contact = Contacts.objects.get(pk=contact_id, user=request.user)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        messages.success(request, "Contact was updated successfully !")
        return redirect(to='contacts:main')
    return render(request, 'contacts/edit.html', context={'form': form, 'contact': contact})


@login_required
def sort(request):
    """
    The sort function is used to sort the contacts by first name.
        It also paginates the contacts so that only 10 are shown per page.
    
    :param request: Get the current request object
    :return: A list of contacts ordered by firstname
    """
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
    The save_csv_to_model function takes a file path to a CSV file and saves the data in that CSV
    file to the Contacts model. The function assumes that the first row of data in the CSV is a header
    row, so it skips over this row when saving each record. If an error occurs while trying to save any 
    record, then all records saved up until that point are rolled back.
    
    :param file_path: Get the path of the file
    :return: A redirect object
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
    """
    The file_uploader function is responsible for uploading a CSV file to the server.
    It also saves the uploaded file in the database and then calls save_csv_to_model function, which saves all contacts from 
    the CSV file to Contacts model.
    
    :param request: Get the request from the user
    :return: The rendered template
    """
    if request.method == 'POST':
        try:
            file = request.FILES.get('file')
            if not file.name.endswith('.csv'):
                messages.warning(request, 'Invalid file format. Please upload a CSV file.')
                return redirect(to='contacts:main')
        except AttributeError:
            messages.warning(request, 'You forgot to choose a file. Please make sure you chose CSV file and upload it.')
            return redirect(to='contacts:main')

        # return HttpResponse('Invalid file format. Please upload a CSV file.')
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