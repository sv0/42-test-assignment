#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.template import Library

register = Library()

@register.simple_tag(name="edit_link")
def get_object_edit_link(object):
    """
    Get the admin change link for an object.

    Example::
        {% edit_link request.user %}
    """
    try:
        return reverse('admin:%s_%s_change'
                       % (object._meta.app_label, object._meta.module_name),
                       args=[object.id])
    except:
        return ''  # shit happens
