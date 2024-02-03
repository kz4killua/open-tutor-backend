from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import JourneySerializer
from .models import Journey

from sections.models import Section

from utilities.reader import extract_text_from_document
from utilities.summary import perform_abstractive_summary
from utilities.evaluation import generate_evaluation_questions


class Journeys(generics.ListCreateAPIView):
    serializer_class = JourneySerializer

    def get_queryset(self):
        return self.request.user.journeys.all()
    
    def post(self, request, *args, **kwargs):

        base_file = request.data.get('base_file')
        title = request.data.get('title')

        # Extract the text content of the uploaded file
        sections = extract_text_from_document(base_file)

        # Generate a summary for each section
        summaries = perform_abstractive_summary(sections)

        # Generate questions and answers for the section
        evaluations = [
            generate_evaluation_questions(text) for text in summaries
        ]

        # Create a journey and the corresponding sections
        journey = Journey.objects.create(
            user=request.user,
            title=title,
            base_file=base_file,
        )

        for summary, evaluation in zip(summaries, evaluations):
            Section.objects.create(
                journey=journey,
                content=summary,
                evaluation=evaluation
            )

        return Response(self.get_serializer(journey).data, status=status.HTTP_202_ACCEPTED)
    

class SingleJourney(generics.RetrieveDestroyAPIView):
    serializer_class = JourneySerializer

    def get_object(self):
        return get_object_or_404(
            Journey, user=self.request.user, pk=self.kwargs['journey_id']
        )