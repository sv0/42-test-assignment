from models import ModelChangeEntry
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


def model_change_logger(sender, action_flag, **kwargs):
    """
        Log that an object has been created or changed or deleted.
    """
    if sender == ModelChangeEntry:
        return
    object_id = getattr(kwargs.get('instance'), 'id', None) \
                if kwargs.get('instance') else None
    try:
        ModelChangeEntry.objects.create(
                content_type_id=ContentType.objects.get_for_model(sender).pk,
                object_id=object_id,
                action_flag=action_flag,
        )
    except:
        # no such table
        # prevent syncdb error
        pass


def model_save_logger(sender, **kwargs):
    action_flag = ADDITION if kwargs.get('created') else CHANGE
    model_change_logger(sender, action_flag, **kwargs)


def model_delete_logger(sender, **kwargs):
    model_change_logger(sender, DELETION, **kwargs)
