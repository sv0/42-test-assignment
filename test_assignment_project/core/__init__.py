from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from signals import model_save_logger, model_delete_logger

post_save.connect(model_save_logger)
post_delete.connect(model_delete_logger)
