from rest_framework.generics import RetrieveAPIView

from django.shortcuts import get_object_or_404

from .serializers import SectionSerializer
from .models import Section


class SingleSection(RetrieveAPIView):
    serializer_class = SectionSerializer

    def get_object(self):
        return get_object_or_404(
            Section, journey__user=self.request.user, pk=self.kwargs['section_id']
        )