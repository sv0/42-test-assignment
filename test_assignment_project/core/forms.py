#-*- coding: utf-8 -*-
from django.contrib.auth.forms import User
from django import forms
from models import Profile
#from widgets import CalendarInput


class ProfileChangeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=30)
    date_of_birth = forms.DateField()

    class Meta:
        model = Profile
        exclude = ('user', )

    class Media:
        js = ('profile/edit_contacts.js',)
