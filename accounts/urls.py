from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.SignUp.as_view(), name='signup'),
    path('token/request', views.RequestToken.as_view(), name='token-request'),
    path('token/verify', views.VerifyToken.as_view(), name='token-verify'),
    path('token/delete', views.DeleteToken.as_view(), name='token-delete'),
]