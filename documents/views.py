from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import DocumentSerializer
from .models import Document


class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer

    def get_object(self):
        return get_object_or_404(Document, user=self.request.user, pk=self.kwargs['pk'])