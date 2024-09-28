import random

from django.http import StreamingHttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DocumentSerializer, MessageSerializer, FlashcardSerializer
from .models import Document, Message, Flashcard

from langchain_core.documents.base import Document as LangChainDocument

from .utilities.vectorstore import upload_langchain_documents_to_vectorstore, delete_vectors_from_vectorstore
from .utilities.messages import construct_user_message, construct_system_message, construct_assistant_message, stream_message_response
from .utilities.preprocessing import extract_text_from_document
from .utilities.flashcards import create_flashcards
from .utilities.feedback import get_feedback
from .utilities.overview import create_overview


class DocumentList(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):

        super().perform_create(serializer)

        # Upload the created document to the vectorstore
        document = serializer.instance
        page_texts = extract_text_from_document(document)
        langchain_documents = [
            LangChainDocument(page_text, metadata={
                'document_id': document.id, 'page_number': page_number
            })
            for page_number, page_text in page_texts.items()
        ]
        pinecone_ids = upload_langchain_documents_to_vectorstore(
            langchain_documents, document.user.id
        )

        document.metadata['pinecone_ids'] = pinecone_ids
        document.metadata['page_texts'] = page_texts
        document.save()


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


class Overview(APIView):

    def get(self, request, *args, **kwargs):

        document = get_object_or_404(Document, user=request.user, pk=self.kwargs['pk'])

        # Create an overview for the document if it does not exist
        if not document.overview:
            document_text = '\n'.join(document.metadata['page_texts'].values())
            document.overview = create_overview(document_text)
            document.save()

        return Response({'overview': document.overview}, status=status.HTTP_200_OK)


class Flashcards(APIView):
    
    def get(self, request, *args, **kwargs):

        document = get_object_or_404(Document, user=request.user, pk=self.kwargs['pk'])

        # Create flashcards for the document if they do not exist
        if not document.flashcards_created:
            document_text = '\n'.join(document.metadata['page_texts'].values())
            create_flashcards(document, document_text)
            document.flashcards_created = True
            document.save()

        # Return 10 random flashcards for evaluation
        flashcards = document.flashcards.order_by('?')[:10]
        serializer = FlashcardSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlashcardsFromText(APIView):

    def post(self, request, *args, **kwargs):
        document = get_object_or_404(Document, user=request.user, pk=self.kwargs['pk'])
        text = request.data.get('text')
        flashcards = create_flashcards(document, text)
        serializer = FlashcardSerializer(flashcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FlashcardFeedback(APIView):
    
    def post(self, request, *args, **kwargs):

        questions_correct = [
            flashcard.front for flashcard in get_list_or_404(
                Flashcard, document__id=self.kwargs['pk'], 
                document__user=request.user, pk__in=request.data.get('correct')
            )
        ]

        questions_wrong = [
            flashcard.front for flashcard in get_list_or_404(
                Flashcard, document__id=self.kwargs['pk'], 
                document__user=request.user, pk__in=request.data.get('wrong')
            )
        ]

        feedback = get_feedback(questions_correct, questions_wrong)

        return Response({'feedback': feedback}, status=status.HTTP_200_OK)