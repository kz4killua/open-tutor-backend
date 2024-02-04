from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files.storage import DefaultStorage
from openlearn.storages import PrivateMediaStorage
import uuid


User = get_user_model()


def select_storage():
    if settings.USE_SPACES:
        return PrivateMediaStorage()
    else:
        return DefaultStorage()


class Journey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journeys')
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    base_file = models.FileField(null=True, storage=select_storage)