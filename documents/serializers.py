from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Document
        fields = ['id', 'name', 'user', 'created', 'file']