import json
from rest_framework import serializers

from .models import Section


class SectionSerializer(serializers.ModelSerializer):
    evaluation = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = "__all__"

    def get_evaluation(self, obj):
        return json.loads(obj.evaluation)
