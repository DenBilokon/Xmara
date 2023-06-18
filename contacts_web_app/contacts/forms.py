from django.forms import TextInput, CharField, ModelForm, EmailField, EmailInput, DateField, DateInput, \
    SelectDateWidget, FileField
from .models import Contacts, File
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from phonenumber_field.widgets import PhoneNumberPrefixWidget

YEARS = [x for x in range(1940, 2020)]


class ContactForm(ModelForm):
    firstname = CharField(min_length=3, max_length=25, required=True,
                          widget=TextInput(attrs={'placeholder': 'Firstname', 'class': "form-control me-2"}))
    lastname = CharField(min_length=3, max_length=25, required=True,
                         widget=TextInput(attrs={'placeholder': 'Lastname', 'class': "form-control me-2"}))
    phone = PhoneNumberField(initial='Ukraine', region='UA',
                             widget=PhoneNumberPrefixWidget(
                                 attrs={'placeholder': 'Phone Number', 'class': "form-control me-2"}))
    email = EmailField(max_length=150, initial="example@email.com",
                       widget=EmailInput(attrs={'placeholder': 'Email', 'class': "form-control me-2"}))
    birthday = DateField(required=True, widget=SelectDateWidget(years=YEARS, attrs={'class': "form-control me-2"}))

    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(),
        }
        model = Contacts
        fields = ['firstname', 'lastname', 'phone', 'email', 'birthday']
