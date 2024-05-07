from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=128)
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name