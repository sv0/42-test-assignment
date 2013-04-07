#-*- coding: utf-8 -*-
from django.forms.widgets import DateInput


class CalendarInput(DateInput):
    class Media:
        css = {
                'screen': ('http://code.jquery.com/ui/1.10.1/themes/base/jquery-ui.css',)
        }
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/jquery-ui.min.js',
              'http://malsup.github.com/jquery.form.js',)
