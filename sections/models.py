from django.db import models
from django.contrib.auth import get_user_model
import uuid

from journeys.models import Journey


User = get_user_model()


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE, related_name='sections')
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True)
    evaluation = models.JSONField(null=True)
    completed = models.BooleanField(default=False)