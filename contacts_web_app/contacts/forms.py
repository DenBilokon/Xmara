from django.forms import TextInput, CharField, ModelForm, EmailField, EmailInput, DateField, DateInput, SelectDateWidget
from .models import Contacts
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from phonenumber_field.widgets import PhoneNumberPrefixWidget

YEARS = [x for x in range(1940, 2020)]


class ContactForm(ModelForm):
    firstname = CharField(min_length=3, max_length=25, required=True,
                          widget=TextInput(attrs={'placeholder': 'Firstname'}))
    lastname = CharField(min_length=3, max_length=25, required=True,
                         widget=TextInput(attrs={'placeholder': 'Lastname'}))
    phone = PhoneNumberField(initial='Ukraine', region='UA',
                             widget=PhoneNumberPrefixWidget(attrs={'placeholder': 'Phone Number'}))
    email = EmailField(max_length=150, required=True, widget=EmailInput(attrs={'placeholder': 'Email'}))
    birthday = DateField(required=True, widget=SelectDateWidget(years=YEARS))

    class Meta:
        widgets = {
            'phone': PhoneNumberPrefixWidget(),
        }
        model = Contacts
        fields = ['firstname', 'lastname', 'phone', 'email', 'birthday']
