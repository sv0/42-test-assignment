#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'jabber', 'skype', 'date_of_birth')


admin.site.register(Profile, ProfileAdmin)
