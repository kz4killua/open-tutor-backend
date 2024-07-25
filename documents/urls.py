from django.urls import path
from . import views


urlpatterns = [
    path('', views.DocumentList.as_view(), name='document-list'),
    path('<int:pk>', views.DocumentDetail.as_view(), name='document-detail'),
    path('<int:pk>/messages', views.DocumentMessages.as_view(), name='document-messages'),
    path('<int:pk>/flashcards', views.PracticeFlashcards.as_view(), name='document-flashcards'),
    path('<int:pk>/flashcards/feedback', views.EvaluationFeedback.as_view(), name='flashcard-feedback'),
]