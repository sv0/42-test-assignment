# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from annoying.decorators import render_to


@render_to("profile/contacts.html")
def home(request):
    user = get_object_or_404(User, pk=2)
    return {'user': user}
