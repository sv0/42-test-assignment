#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


def get_project_models():
    for content_type in ContentType.objects.all():
        model_class = content_type.model_class()
        yield (model_class.__name__, model_class._default_manager.count())


class Command(BaseCommand):
    help = "Shows models and counts them objecs"

    def handle(self, *args, **options):
        for class_name, obj_count in get_project_models():
            model_and_count = "%-15s %10d\n" % (class_name, obj_count)
            self.stdout.write(model_and_count)
            self.stderr.write("error: %s" % model_and_count)
