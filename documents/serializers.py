from rest_framework import serializers
from .models import Document, Message


class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Document
        fields = ['id', 'name', 'user', 'created', 'file']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'quote', 'created']