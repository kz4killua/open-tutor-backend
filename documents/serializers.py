from rest_framework import serializers
from .models import Document, Message


class DocumentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    size = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'name', 'user', 'created', 'file', 'size']

    def get_size(self, obj):
        return obj.file.size


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'quote', 'created']