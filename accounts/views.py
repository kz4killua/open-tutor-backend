from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status


User = get_user_model()


class SignUp(generics.CreateAPIView):
    """Create an account."""
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSerializer


class RequestToken(ObtainAuthToken):
    """Request an API token."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        # Get the user's email and password
        email = request.data.get('email')
        password = request.data.get('password')

        # Find any matching users
        user = authenticate(username=email, password=password)
        
        # Handle invalid login details
        if user is None:
            raise AuthenticationFailed()
        
        # Retrieve the user's token
        token, _ = Token.objects.get_or_create(user=user)

        # Update the user's last_login
        user.last_login = timezone.now()
        user.save()

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class DeleteToken(APIView):
    """Sign out and destroy access tokens."""

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            pass
        else:
            token.delete()

        return Response(status=status.HTTP_200_OK)


class VerifyToken(APIView):
    """Verify that an access token is valid."""
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        try:
            Token.objects.get(key=request.data.get('token'))
        except Token.DoesNotExist:
            raise AuthenticationFailed()
        else:
            return Response(status=status.HTTP_200_OK)