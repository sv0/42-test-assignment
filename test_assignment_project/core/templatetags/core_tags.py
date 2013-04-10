#-*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template import Library

register = Library()


@register.simple_tag(name="edit_link")
def get_object_edit_link(obj):
    """
    Get the admin change link for an object.

    Example::
        {% edit_link request.user %}
    """
    try:
        obj_content_type = ContentType.objects.get_for_model(obj)

        return reverse('admin:%s_%s_change'
                       % (
                           obj_content_type.app_label,
                           obj_content_type.name
                         ),
                       args=[obj.id])
    except:
        return ''  # shit happens
