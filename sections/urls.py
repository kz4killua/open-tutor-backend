from django.urls import path
from . import views


urlpatterns = [
    path('<uuid:section_id>', views.SingleSection.as_view(), name='single-section'),
]