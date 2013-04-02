#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals


class Profile(models.Model):
    user = models.ForeignKey(User)
    date_of_birth = models.DateField()
    bio = models.TextField(max_length=1024, verbose_name=_(u'Biography'),
                           blank=True)
    jabber = models.EmailField(blank=True)
    skype = models.CharField(max_length=64, blank=True)
    other_contacts = models.TextField(max_length=512, blank=True)
    photo = models.ImageField(upload_to='photos', blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user.username


def create_profile(sender, instance, *args, **kwargs):
    """Create user's Profile after User was created."""
    try:
        Profile.objects.get(user=instance)
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
#signals.post_save.connect(create_profile, sender=User)
