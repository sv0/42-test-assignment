#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Profile, MyHttpRequest, ModelChangeEntry


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'jabber', 'skype', 'date_of_birth')


class ModelChangeEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'action_flag', 'content_type', 'action_time')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(MyHttpRequest)
admin.site.register(ModelChangeEntry, ModelChangeEntryAdmin)
