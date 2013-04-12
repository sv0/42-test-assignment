#-*- coding: utf-8 -*-
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.widgets import DateInput, ClearableFileInput
#from django.utils.safestring import mark_safe

class CalendarInput(DateInput):
    class Media:
        css = {
                'screen': ('http://code.jquery.com/ui/1.10.1/themes/base/jquery-ui.css',)
        }
        js = ('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
              'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.1/jquery-ui.min.js',
              'http://malsup.github.com/jquery.form.js',)

    # copypasted from http://nanvel.name/weblog/django-datepicker-widget/ 
    def __init__(self, params='', attrs=None):
        self.params = params
        super(CalendarInput, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(CalendarInput, self).render(name, value, attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({%s});
            </script>'''%(name, self.params,))


class ProfilePhotoInput(ClearableFileInput):
    class Media:
        js = ('profile/filereader.js',)
