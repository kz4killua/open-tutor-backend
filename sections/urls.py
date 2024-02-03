from django.urls import path
from . import views


urlpatterns = [
    path('<uuid:section_id>', views.SingleSection.as_view(), name='single-section'),
    path('<uuid:section_id>/chat', views.SectionChat.as_view(), name='section-view'),

]