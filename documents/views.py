import random

from django.http import StreamingHttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
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
    

class PracticeFlashcards(APIView):
    serializer_class = FlashcardSerializer
    
    def get(self, request, *args, **kwargs):
        
        document = get_object_or_404(Document, user=request.user, pk=self.kwargs['pk'])
        num_pages = len(document.metadata['page_texts'])
        max_flashcards = 10
        evaluation_questions = []
        shuffled_pages = list(range(num_pages))
        random.shuffle(shuffled_pages)

        # Pick out the maximum number of flashcards from random pages
        for page_number in shuffled_pages:
            page_flashcards = document.flashcards.filter(
                referenced_page_number=page_number
            )
            
            # Create the flashcards if they have not been created
            if not page_flashcards.exists():
                create_flashcards(document, page_number)
                page_flashcards = document.flashcards.filter(
                    referenced_page_number=page_number
                )

            evaluation_questions.extend(page_flashcards)

            if len(evaluation_questions) >= max_flashcards:
                evaluation_questions = evaluation_questions[:max_flashcards]
                break

        serializer = FlashcardSerializer(evaluation_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class EvaluationFeedback(APIView):
    serializer_class = FlashcardSerializer
    
    def post(self, request, *args, **kwargs):

        questions_correct = [
            get_object_or_404(
                Flashcard, document__id=self.kwargs['pk'], 
                document__user=request.user, pk=flashcard_id
            ).front
            for flashcard_id in request.data.get('correct')
        ]
        questions_wrong = [
            get_object_or_404(
                Flashcard, document__id=self.kwargs['pk'], 
                document__user=request.user, pk=flashcard_id
            ).front
            for flashcard_id in request.data.get('wrong')
        ]

        feedback = get_feedback(questions_correct, questions_wrong)

        return Response({'feedback': feedback}, status=status.HTTP_200_OK)