from django.urls import path
from . import views


urlpatterns = [
    path('token/request', views.RequestToken.as_view(), name='request-token'),
    path('token/delete', views.DeleteToken.as_view(), name='delete-token'),
    path('signup', views.SignUp.as_view(), name='signup'),
]