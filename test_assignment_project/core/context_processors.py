#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf import settings

def settings_context_processor(request):
    return dict(settings=settings)
