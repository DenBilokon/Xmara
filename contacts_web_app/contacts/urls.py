from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.main, name='main'),
    path('contacts', views.contacts, name='contacts'),
    path('sort', views.sort, name='sort'),
    path('birthday', views.birthday, name='birthday'),
    path('contacts/edit/<int:contact_id>', views.edit, name='edit'),
    path('delete/<int:contact_id>', views.delete_contact, name='delete_contact'),
    path('search_contact', views.search_contact, name='search_contact')
]