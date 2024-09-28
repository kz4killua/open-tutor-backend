from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocumentList.as_view(), name='document-list'),
    path('<int:pk>', views.DocumentDetail.as_view(), name='document-detail'),
    path('<int:pk>/messages', views.DocumentMessages.as_view(), name='document-messages'),
    path('<int:pk>/flashcards', views.Flashcards.as_view(), name='flashcards'),
    path('<int:pk>/flashcards/from-text', views.FlashcardsFromText.as_view(), name='flashcards-from-text'),
    path('<int:pk>/flashcards/feedback', views.FlashcardFeedback.as_view(), name='flashcard-feedback'),
]