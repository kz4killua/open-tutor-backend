from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .serializers import SectionSerializer
from .models import Section

from utilities.answering import generate_response_to_question


class SingleSection(RetrieveAPIView):
    serializer_class = SectionSerializer

    def get_object(self):
        return get_object_or_404(
            Section, journey__user=self.request.user, pk=self.kwargs['section_id']
        )
    

class SectionChat(APIView):

    def post(self, request, *args, **kwargs):

        question = request.data.get('question')

        # Get the queried section
        section = get_object_or_404(
            Section, journey__user=self.request.user, pk=self.kwargs['section_id']
        )

        # Generate an answer
        answer = generate_response_to_question(question, section.content)

        return Response({'answer': answer})