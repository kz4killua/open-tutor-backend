from django.db import models
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()


class Journey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journeys')
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    base_file = models.FileField(null=True)