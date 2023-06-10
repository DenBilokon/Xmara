from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contacts
from datetime import date, datetime, timedelta


# Create your views here.

def main(request):
    contacts = Contacts.objects.all()
    return render(request, 'contacts/index.html', context={'contacts': contacts})


def search_contact(request):
    return render(request, 'contacts/search_contact.html', )

def birthday(request):
    contacts_all = Contacts.objects.all()
    current_year = date.today().year
    birthday_list = []
    show = []
    for i in contacts_all:
        if date.today() < (datetime.strptime(i.birthday, '%Y-%m-%d').date()).replace(current_year) < date.today() + timedelta(7):
            birthday_list.append(i)


    # for i in res:
    #     if date.today() < i < date.today() + timedelta(7):
    #         show.append(i)

    return render(request, 'contacts/birthday.html',
                  context={'current_day': current_year, 'birthday_list': birthday_list, 'today': date.today(), 'show': show})
    # next_week = [(current_day + timedelta(i)).strftime('%B %d') for i in range(7)]
    # list_of_contacts = [contact for contact in contacts_all if contact.birthday.date().strftime('%B %d') in next_week]
    # return render(request, 'contacts/index.html', context={'list_of_contacts': list_of_contacts})


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, )
        if form.is_valid():
            form.save()
            return redirect(to='contacts:main')
        else:
            return render(request, 'contacts/contact.html', {'form': form})
    return render(request, 'contacts/contact.html', {'form': ContactForm()})


# def info(request):
#     contacts = Contacts.objects.all()
#     return render()

def delete_contact(request, contact_id):
    Contacts.objects.get(pk=contact_id).delete()
    return redirect(to='contacts:main')


# def edit(request, contact_id):
#     if request.method == 'POST':
#         form = ContactForm(request.POST, )
#         firstname = request.POST.get('firstname')
#         lastname = request.POST.get('lastname')
#         phone = request.POST.get('phone')
#         firstname = request.POST.get('firstname')
#         email = request.POST.get('email')
#         birthday = request.POST.get('birthday')
#         if form.is_valid():
#             form.save()
#             return redirect(to='contacts:main')
#
#         Contacts.objects.filter(pk=contact_id).update(firstname=firstname, lastname=lastname, phone=phone, email=email,
#                                                       birthday=birthday)
#         return redirect(to='contacts:main')
#
#     contact = Contacts.objects.filter(pk=contact_id).first()
#     return render(request, 'contacts/edit.html',
#                   context={'title': 'Update', 'contact': contact, 'form': ContactForm(), 'name': contact.firstname,
#                            'phone': str(contact.phone)[:4]})

def edit(request, contact_id):
    contact = Contacts.objects.get(pk=contact_id)
    form = ContactForm(request.POST or None, instance=contact)
    if form.is_valid():
        form.save()
        return redirect(to='contacts:main')
    return render(request, 'contacts/edit.html', context={'form': form, 'contact': contact})


def sort(request):
    contacts = Contacts.objects.all().order_by('firstname').values()
    return render(request, 'contacts/index.html', context={'contacts': contacts})
