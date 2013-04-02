# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.simple import redirect_to
from annoying.decorators import render_to
from models import MyHttpRequest


@render_to("profile/contacts.html")
def home(request):
    user = get_object_or_404(User, pk=2)
    return {'user': user}


@render_to("my_http_request/first_requests.html")
def first_requests(request):
    limit = 10
    request_list = MyHttpRequest.objects.all()[:limit]
    return {'request_list': request_list, 'limit': limit}
