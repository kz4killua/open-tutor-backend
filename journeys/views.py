from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import JourneySerializer
from .models import Journey

from sections.models import Section
from sections.serializers import SectionSerializer

from .tasks import create_journey_task


class Journeys(generics.ListCreateAPIView):
    serializer_class = JourneySerializer

    def get_queryset(self):
        return self.request.user.journeys.all()
    
    def post(self, request, *args, **kwargs):

        base_file = request.data.get('base_file')
        title = request.data.get('title')

        # Create a journey
        journey = Journey.objects.create(
            user=request.user,
            title=title,
            base_file=base_file,
        )

        # Set the task to initialize journey sections
        create_journey_task.delay(
            journey.id
        )

        return Response(self.get_serializer(journey).data, status=status.HTTP_202_ACCEPTED)


class SingleJourney(generics.RetrieveDestroyAPIView):
    serializer_class = JourneySerializer

    def get_object(self):
        return get_object_or_404(
            Journey, user=self.request.user, pk=self.kwargs['journey_id']
        )


class JourneySections(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        return get_object_or_404(
            Journey, user=self.request.user, pk=self.kwargs['journey_id']
        ).sections