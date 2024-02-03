from rest_framework import serializers

from .models import Journey

from sections.serializers import SectionSerializer


class JourneySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sections = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Journey
        fields = "__all__"
