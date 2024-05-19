from django.http import StreamingHttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework import serializers
from .serializers import DocumentSerializer, MessageSerializer
from .models import Document, Message

from .utilities.vectorstore import upload_open_tutor_document_to_vectorstore, delete_vectors_from_vectorstore
from .utilities.messages import construct_user_message, construct_system_message, construct_assistant_message, stream_message_response


class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Upload the created document to the vectorstore
        document = Document.objects.get(id=response.data['id'])
        pinecone_ids = upload_open_tutor_document_to_vectorstore(
            document
        )
        document.metadata['pinecone_ids'] = pinecone_ids
        document.save()

        return response


class DocumentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer

    def get_object(self):
        return get_object_or_404(Document, user=self.request.user, pk=self.kwargs['pk'])
    
    def delete(self, request, *args, **kwargs):

        # Before deletion, remove vectors from the vectorstore
        document = self.get_object()
        delete_vectors_from_vectorstore(
            document.metadata['pinecone_ids'], document.user.pk
        )

        return super().delete(request, *args, **kwargs)


class DocumentMessages(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_object(self):
        return get_object_or_404(Document, user=self.request.user, pk=self.kwargs['pk'])

    def get_queryset(self):
        document = self.get_object()
        return document.messages.filter(
            role__in=("user", "assistant")
        )

    def post(self, request, *args, **kwargs):

        document = self.get_object()
        user_message = construct_user_message(
            document, request.data.get('query'), request.data.get('quote')
        )

        # Ensure that the user_message is valid before proceeding
        data = MessageSerializer(user_message).data
        MessageSerializer(data=data).is_valid(raise_exception=True)

        system_message = construct_system_message(user_message)
        assistant_message = construct_assistant_message(user_message)
        message_history = document.messages.filter(
            role__in=("user", "assistant")
        )

        response = StreamingHttpResponse(
            stream_message_response(user_message, system_message, assistant_message, message_history)
        )
        response['Content-Type'] = 'text/event-stream'

        return response