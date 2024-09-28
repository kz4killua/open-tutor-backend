from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator


User = get_user_model()


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=128)
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)
    flashcards_created = models.BooleanField(default=False)
    overview = models.TextField(max_length=2048, blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Message(models.Model):

    MESSAGE_ROLE_CHOICES = {
        "system": "system",
        "assistant": "assistant",
        "user": "user"
    }

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=16, choices=MESSAGE_ROLE_CHOICES)
    content = models.TextField(max_length=1024, validators=[
        MaxLengthValidator(1024, "Message content cannot exceed 1024 characters.")
    ])
    quote = models.TextField(max_length=1024, validators=[
        MaxLengthValidator(1024, "Quoted content cannot exceed 1024 characters.")
    ], blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]


class Flashcard(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='flashcards')
    front = models.TextField(max_length=1024)
    back = models.TextField(max_length=1024)