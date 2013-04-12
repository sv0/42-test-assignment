#-*- coding: utf-8 -*-
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals

ACTION_FLAG_CHOICES = (
    (ADDITION, 'ADDITION'),
    (CHANGE, 'CHANGE'),
    (DELETION, 'DELETION'),
)

NUM_OF_PRIORITIES = 10
PRIORITY_CHOICES = tuple([(x, "Priority %s" % str(x + 1))
                         for x in range(NUM_OF_PRIORITIES)])


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


class MyHttpRequestManager(models.Manager):
    def create_from_request(self, request):
        self.create(host=request.get_host(),
                    path=request.path,
                    method=request.method,
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    remote_addr=request.META.get('REMOTE_ADDR'),
                    is_secure=request.is_secure(),
                    is_ajax=request.is_ajax())


class MyHttpRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    host = models.CharField(max_length=256)
    path = models.CharField(max_length=256)
    method = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=256, blank=True, null=True)
    remote_addr = models.IPAddressField()
    remote_addr_fwd = models.IPAddressField(blank=True, null=True)
    cookies = models.TextField(blank=True, null=True)
    get = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    raw_post = models.TextField(blank=True, null=True)
    is_secure = models.BooleanField()
    is_ajax = models.BooleanField()
    priority = models.SmallIntegerField(_('Priority'),
                                        choices=PRIORITY_CHOICES,
                                        default=0)
    objects = MyHttpRequestManager()

    def __unicode__(self):
        return u"%s%s" % (self.host, self.path)


class ModelChangeEntry(models.Model):
    action_time = models.DateTimeField(_('action time'), auto_now=True)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(_('object id'), blank=True, null=True)
    action_flag = models.PositiveSmallIntegerField(
                    _('action flag'),
                    choices=ACTION_FLAG_CHOICES
    )
